"""
K8s 权限绑定扫描器模块
======================
负责扫描集群中所有的 RoleBinding 和 ClusterRoleBinding，
提取与 ServiceAccount 相关的绑定信息。
"""

from kubernetes import client
from kubernetes.client.rest import ApiException
from typing import List, Dict


def scan_role_bindings(rbac_api: client.RbacAuthorizationV1Api) -> List[Dict]:
    """
    扫描集群中所有 Namespace 下的 RoleBinding。

    遍历每个 RoleBinding，筛选出 subject 类型为 ServiceAccount 的绑定，
    提取关键信息用于后续的权限分析。

    Args:
        rbac_api: RbacAuthorizationV1Api 实例

    Returns:
        List[Dict]: 包含以下字段的字典列表：
            - namespace: 绑定所在的命名空间
            - name: 绑定名称
            - binding_type: 绑定类型（固定为 "RoleBinding"）
            - role_name: 绑定的角色名称
            - role_kind: 角色类型（Role 或 ClusterRole）
            - subjects: 绑定的主体列表（ServiceAccount 信息）
    """
    bindings = []
    try:
        # 获取所有 Namespace 下的 RoleBinding
        # list_role_binding_for_all_namespaces() 会返回集群中所有的 RoleBinding
        role_bindings = rbac_api.list_role_binding_for_all_namespaces()
        print(f"[ℹ] 发现 {len(role_bindings.items)} 个 RoleBinding")

        for rb in role_bindings.items:
            # 提取绑定元数据
            binding_info = {
                "namespace": rb.metadata.namespace,      # 绑定所在的命名空间
                "name": rb.metadata.name,                 # 绑定名称
                "binding_type": "RoleBinding",            # 绑定类型
                "role_name": rb.role_ref.name,            # 绑定的角色名称
                "role_kind": rb.role_ref.kind,            # 角色类型（Role/ClusterRole）
                "subjects": []                            # 绑定的主体列表
            }

            # 提取 subjects（绑定的主体，如 ServiceAccount、User、Group）
            if rb.subjects:
                for subject in rb.subjects:
                    binding_info["subjects"].append({
                        "kind": subject.kind,              # 主体类型（ServiceAccount/User/Group）
                        "name": subject.name,              # 主体名称
                        "namespace": subject.namespace     # 主体所在的命名空间（仅 ServiceAccount 有）
                    })

            bindings.append(binding_info)

    except ApiException as e:
        print(f"[✗] 扫描 RoleBinding 失败: {e}")
        return []

    return bindings


def scan_cluster_role_bindings(rbac_api: client.RbacAuthorizationV1Api) -> List[Dict]:
    """
    扫描集群中所有的 ClusterRoleBinding。

    ClusterRoleBinding 是集群级别的绑定，不局限于特定 Namespace，
    因此权限影响范围更大，需要特别关注。

    Args:
        rbac_api: RbacAuthorizationV1Api 实例

    Returns:
        List[Dict]: 包含以下字段的字典列表：
            - namespace: 固定为 "cluster-wide"（表示集群范围）
            - name: 绑定名称
            - binding_type: 绑定类型（固定为 "ClusterRoleBinding"）
            - role_name: 绑定的集群角色名称
            - role_kind: 角色类型（固定为 "ClusterRole"）
            - subjects: 绑定的主体列表
    """
    bindings = []
    try:
        # 获取所有 ClusterRoleBinding
        cluster_role_bindings = rbac_api.list_cluster_role_binding()
        print(f"[ℹ] 发现 {len(cluster_role_bindings.items)} 个 ClusterRoleBinding")

        for crb in cluster_role_bindings.items:
            # 提取绑定元数据
            binding_info = {
                "namespace": "cluster-wide",               # 集群范围，不限定 Namespace
                "name": crb.metadata.name,                 # 绑定名称
                "binding_type": "ClusterRoleBinding",      # 绑定类型
                "role_name": crb.role_ref.name,            # 绑定的集群角色名称
                "role_kind": crb.role_ref.kind,            # 角色类型（固定为 ClusterRole）
                "subjects": []                             # 绑定的主体列表
            }

            # 提取 subjects
            if crb.subjects:
                for subject in crb.subjects:
                    binding_info["subjects"].append({
                        "kind": subject.kind,
                        "name": subject.name,
                        "namespace": subject.namespace
                    })

            bindings.append(binding_info)

    except ApiException as e:
        print(f"[✗] 扫描 ClusterRoleBinding 失败: {e}")
        return []

    return bindings


def scan_all_bindings(rbac_api: client.RbacAuthorizationV1Api) -> List[Dict]:
    """
    扫描集群中所有的权限绑定（RoleBinding + ClusterRoleBinding）。

    这是扫描器的统一入口，合并两种绑定的扫描结果。

    Args:
        rbac_api: RbacAuthorizationV1Api 实例

    Returns:
        List[Dict]: 所有绑定的信息列表
    """
    print("\n" + "="*60)
    print("  开始扫描 K8s 权限绑定")
    print("="*60)

    # 扫描 RoleBinding
    role_bindings = scan_role_bindings(rbac_api)
    print(f"  RoleBinding 数量: {len(role_bindings)}")

    # 扫描 ClusterRoleBinding
    cluster_role_bindings = scan_cluster_role_bindings(rbac_api)
    print(f"  ClusterRoleBinding 数量: {len(cluster_role_bindings)}")

    # 合并结果
    all_bindings = role_bindings + cluster_role_bindings
    print(f"  绑定总数: {len(all_bindings)}")
    print("="*60 + "\n")

    return all_bindings
