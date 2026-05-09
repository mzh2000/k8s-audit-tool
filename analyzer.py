"""
K8s 权限分析器模块
==================
负责分析扫描到的 RoleBinding 和 ClusterRoleBinding，
识别出权限过大的 ServiceAccount。

核心判断逻辑：
1. 筛选出绑定到高风险角色（如 cluster-admin）的 ServiceAccount
2. 排除系统 Namespace（kube-*, openshift-* 等）中的 ServiceAccount
3. 对非系统 ServiceAccount 标记风险等级
"""

from typing import List, Dict


# 高风险角色列表：这些角色拥有集群级别的超级管理员权限
# 非系统 ServiceAccount 绑定这些角色属于高风险行为
HIGH_RISK_ROLES = [
    "cluster-admin",    # 集群管理员，拥有所有权限
    "admin",            # 管理员权限（在特定 Namespace 内拥有大部分权限）
    "edit",             # 编辑权限（可读写资源，但不能修改 RBAC 和配额）
    "sudo",             # 某些自定义的超级用户角色
    "super-admin",      # 某些自定义的超级管理员角色
    "root",             # 某些自定义的根角色
]

# 系统 Namespace 前缀列表：这些 Namespace 中的 ServiceAccount 属于系统组件
# 系统组件的权限绑定通常是正常的，不需要告警
SYSTEM_NAMESPACE_PREFIXES = [
    "kube-",            # Kubernetes 系统组件（kube-system, kube-public, kube-node-lease）
    "openshift-",       # OpenShift 系统组件
    "openshift",        # OpenShift 核心 Namespace
    "calico-",          # Calico 网络组件
    "cilium-",          # Cilium 网络组件
    "istio-",           # Istio 服务网格组件
    "knative-",         # Knative 服务组件
    "flux-",            # Flux CD 组件
    "argocd",           # ArgoCD 组件
    "cert-manager",     # cert-manager 证书管理组件
    "velero",           # Velero 备份组件
    "rook-",            # Rook 存储组件
    "longhorn-",        # Longhorn 存储组件
    "metallb-",         # MetalLB 负载均衡组件
    "ingress-",         # Ingress 控制器组件
    "monitoring-",      # 监控组件
    "logging-",         # 日志组件
]


def is_system_namespace(namespace: str) -> bool:
    """
    判断给定的 Namespace 是否为系统 Namespace。

    系统 Namespace 中的 ServiceAccount 通常是集群组件正常运行所需的，
    它们的权限绑定属于正常行为，不需要告警。

    Args:
        namespace: Namespace 名称

    Returns:
        bool: 如果是系统 Namespace 返回 True，否则返回 False
    """
    if not namespace:
        return False

    # 检查 Namespace 名称是否以系统前缀开头
    for prefix in SYSTEM_NAMESPACE_PREFIXES:
        if namespace.startswith(prefix):
            return True

    return False


def is_high_risk_role(role_name: str) -> bool:
    """
    判断给定的角色是否为高风险角色。

    Args:
        role_name: 角色名称

    Returns:
        bool: 如果是高风险角色返回 True，否则返回 False
    """
    return role_name.lower() in HIGH_RISK_ROLES


def analyze_bindings(all_bindings: List[Dict]) -> List[Dict]:
    """
    分析所有权限绑定，识别出权限过大的 ServiceAccount。

    分析逻辑：
    1. 遍历所有绑定，筛选出 subject 类型为 ServiceAccount 的条目
    2. 检查绑定的角色是否属于高风险角色
    3. 检查 ServiceAccount 所在的 Namespace 是否为系统 Namespace
    4. 对非系统 Namespace 中绑定高风险角色的 ServiceAccount 标记风险等级

    Args:
        all_bindings: scan_all_bindings() 返回的绑定信息列表

    Returns:
        List[Dict]: 审计结果列表，每个元素包含：
            - namespace: 绑定所在的命名空间
            - binding_name: 绑定名称
            - binding_type: 绑定类型（RoleBinding / ClusterRoleBinding）
            - role_name: 绑定的角色名称
            - role_kind: 角色类型（Role / ClusterRole）
            - sa_name: ServiceAccount 名称
            - sa_namespace: ServiceAccount 所在的命名空间
            - risk_level: 风险等级（🔴 高风险 / 🟡 中风险 / 🟢 低风险）
            - description: 风险描述
    """
    print("\n" + "="*60)
    print("  开始分析权限绑定")
    print("="*60)

    audit_results = []

    for binding in all_bindings:
        # 获取绑定的基本信息
        binding_namespace = binding.get("namespace", "")
        binding_name = binding.get("name", "")
        binding_type = binding.get("binding_type", "")
        role_name = binding.get("role_name", "")
        role_kind = binding.get("role_kind", "")
        subjects = binding.get("subjects", [])

        # 遍历所有 subjects，只关注 ServiceAccount 类型
        for subject in subjects:
            if subject.get("kind") != "ServiceAccount":
                continue  # 跳过 User 和 Group 类型的主体

            sa_name = subject.get("name", "")
            sa_namespace = subject.get("namespace", "")

            # 判断 ServiceAccount 是否在系统 Namespace 中
            is_system_sa = is_system_namespace(sa_namespace)

            # 判断绑定的角色是否为高风险角色
            is_high_risk = is_high_risk_role(role_name)

            # 确定风险等级和描述
            risk_level = "🟢 低风险"
            description = "正常权限绑定"

            if is_high_risk and not is_system_sa:
                # 高风险：非系统 ServiceAccount 绑定了高风险角色
                risk_level = "🔴 高风险"
                description = (
                    f"非系统 ServiceAccount '{sa_name}' "
                    f"通过 {binding_type} 绑定了高风险角色 '{role_name}'，"
                    f"可能拥有过大的集群权限"
                )
            elif is_high_risk and is_system_sa:
                # 中风险：系统 ServiceAccount 绑定了高风险角色（通常是正常的）
                risk_level = "🟡 中风险"
                description = (
                    f"系统 ServiceAccount '{sa_name}' "
                    f"绑定了高风险角色 '{role_name}'，"
                    f"请确认是否为必要权限"
                )
            elif not is_high_risk and not is_system_sa:
                # 低风险：非系统 ServiceAccount 绑定了普通角色
                risk_level = "🟢 低风险"
                description = (
                    f"ServiceAccount '{sa_name}' "
                    f"绑定了角色 '{role_name}'，权限在合理范围内"
                )

            # 构建审计结果条目
            result_item = {
                "namespace": binding_namespace,
                "binding_name": binding_name,
                "binding_type": binding_type,
                "role_name": role_name,
                "role_kind": role_kind,
                "sa_name": sa_name,
                "sa_namespace": sa_namespace or binding_namespace,
                "risk_level": risk_level,
                "description": description
            }

            audit_results.append(result_item)

    # 统计风险分布
    high_risk_count = sum(1 for r in audit_results if "🔴" in r["risk_level"])
    medium_risk_count = sum(1 for r in audit_results if "🟡" in r["risk_level"])
    low_risk_count = sum(1 for r in audit_results if "🟢" in r["risk_level"])

    print(f"  ServiceAccount 绑定总数: {len(audit_results)}")
    print(f"  🔴 高风险: {high_risk_count}")
    print(f"  🟡 中风险: {medium_risk_count}")
    print(f"  🟢 低风险: {low_risk_count}")
    print("="*60 + "\n")

    return audit_results


def get_high_risk_results(audit_results: List[Dict]) -> List[Dict]:
    """
    从审计结果中筛选出高风险条目。

    Args:
        audit_results: analyze_bindings() 返回的审计结果列表

    Returns:
        List[Dict]: 高风险条目列表
    """
    return [r for r in audit_results if "🔴" in r["risk_level"]]
