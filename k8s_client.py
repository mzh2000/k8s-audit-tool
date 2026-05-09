"""
K8s 客户端连接模块
===================
负责加载 kubeconfig 并初始化 Kubernetes API 客户端。
支持从默认路径 (~/.kube/config) 或环境变量 KUBECONFIG 加载配置。
"""

from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Tuple


def get_rbac_api() -> Tuple[client.RbacAuthorizationV1Api, client.CoreV1Api]:
    """
    初始化并返回 Kubernetes RBAC API 客户端和 Core API 客户端。

    流程：
    1. 尝试加载默认 kubeconfig（~/.kube/config）
    2. 如果失败，尝试加载集群内配置（适用于 Pod 内运行）
    3. 返回 RbacAuthorizationV1Api 和 CoreV1Api 实例

    Returns:
        Tuple[client.RbacAuthorizationV1Api, client.CoreV1Api]:
        - rbac_api: 用于操作 RoleBinding / ClusterRoleBinding 的 API
        - core_api: 用于获取 Namespace 等基础资源的 API

    Raises:
        Exception: 当无法加载任何有效的 Kubernetes 配置时抛出
    """
    try:
        # 尝试加载默认的 kubeconfig 文件
        # 通常位于 ~/.kube/config，也可以通过 KUBECONFIG 环境变量指定
        config.load_kube_config()
        print("[✓] 成功加载 kubeconfig 配置")
    except Exception as e:
        # 如果 kubeconfig 加载失败，尝试集群内配置
        # 这适用于在 K8s Pod 内部运行的情况
        try:
            config.load_incluster_config()
            print("[✓] 成功加载集群内配置")
        except Exception as inner_e:
            error_msg = (
                f"[✗] 无法加载 Kubernetes 配置\n"
                f"  原因: {str(e)}\n"
                f"  请确保:\n"
                f"  1. kubeconfig 文件存在于 ~/.kube/config\n"
                f"  2. 或已设置 KUBECONFIG 环境变量\n"
                f"  3. 或当前在 K8s Pod 内运行"
            )
            raise Exception(error_msg) from inner_e

    # 创建 RBAC API 客户端 - 用于操作 RoleBinding 和 ClusterRoleBinding
    rbac_api = client.RbacAuthorizationV1Api()
    # 创建 Core API 客户端 - 用于获取 Namespace 等基础资源
    core_api = client.CoreV1Api()

    return rbac_api, core_api


def list_all_namespaces(core_api: client.CoreV1Api) -> list:
    """
    获取集群中所有 Namespace 的名称列表。

    Args:
        core_api: CoreV1Api 实例

    Returns:
        list: 所有 Namespace 的名称列表
    """
    try:
        namespaces = core_api.list_namespace()
        ns_list = [ns.metadata.name for ns in namespaces.items]
        print(f"[ℹ] 集群中共发现 {len(ns_list)} 个 Namespace")
        return ns_list
    except ApiException as e:
        print(f"[✗] 获取 Namespace 列表失败: {e}")
        return []
