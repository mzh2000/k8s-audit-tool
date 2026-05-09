"""
K8s 客户端连接模块
===================
负责加载 kubeconfig 并初始化 Kubernetes API 客户端。
支持从默认路径 (~/.kube/config) 或环境变量 KUBECONFIG 加载配置。
支持自签名证书的集群（如本地 kubeadm 集群）。
"""

from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Tuple
import urllib3


# 禁用 SSL 警告（针对自签名证书）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_rbac_api() -> Tuple[client.RbacAuthorizationV1Api, client.CoreV1Api]:
    """
    初始化并返回 Kubernetes RBAC API 客户端和 Core API 客户端。

    流程：
    1. 尝试加载默认 kubeconfig（~/.kube/config）
    2. 如果 SSL 验证失败，尝试使用 verify_ssl=False（适用于自签名证书集群）
    3. 如果仍然失败，尝试加载集群内配置（适用于 Pod 内运行）
    4. 返回 RbacAuthorizationV1Api 和 CoreV1Api 实例

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
        print(f"[!] 加载 kubeconfig 失败: {e}")
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

    # 创建 API 客户端并测试连接
    rbac_api = client.RbacAuthorizationV1Api()
    core_api = client.CoreV1Api()

    try:
        # 测试连接：尝试获取 API 资源列表
        core_api.get_api_resources()
        print("[✓] API 客户端创建成功，SSL 验证通过")
    except Exception as e:
        ssl_error_keywords = [
            "SSL", "ssl", "CERTIFICATE_VERIFY_FAILED",
            "certificate verify failed", "self-signed certificate",
            "SSLError", "MaxRetryError"
        ]
        if any(kw in str(e) for kw in ssl_error_keywords):
            print("[!] 检测到自签名证书错误，尝试使用 SSL 验证跳过模式...")
            rbac_api, core_api = _create_api_with_ssl_skip()
        else:
            print(f"[!] API 调用失败（非 SSL 问题）: {e}")

    return rbac_api, core_api


def _create_api_with_ssl_skip() -> Tuple[client.RbacAuthorizationV1Api, client.CoreV1Api]:
    """
    创建 API 客户端并跳过 SSL 验证（适用于自签名证书的集群）。

    从 kubeconfig 加载配置后，设置 verify_ssl=False 以跳过证书验证。

    Returns:
        Tuple[client.RbacAuthorizationV1Api, client.CoreV1Api]:
        - rbac_api: RBAC API 客户端
        - core_api: Core API 客户端
    """
    # 重新加载配置
    config.load_kube_config()

    # 获取当前配置并设置跳过 SSL 验证
    # kubernetes 客户端库默认使用单例配置
    default_config = client.Configuration.get_default_copy()
    default_config.verify_ssl = False
    # 注意：不设置 host，让它使用 kubeconfig 中的 server 地址
    client.Configuration.set_default(default_config)

    print("[✓] 已配置跳过 SSL 验证模式（适用于自签名证书）")

    # 使用新配置创建 API 客户端
    rbac_api = client.RbacAuthorizationV1Api()
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
