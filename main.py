"""
K8s 安全审计工具 - 主入口
=========================
Kubernetes 集群权限审计工具，用于扫描和分析集群中的
RoleBinding 和 ClusterRoleBinding，识别权限过大的 ServiceAccount。

使用方法：
    python main.py

前置条件：
    1. 已配置 kubectl（~/.kube/config 文件存在且有效）
    2. 对集群有足够的 RBAC 读取权限
    3. 已安装 Python 依赖（pip install -r requirements.txt）

工作流程：
    1. 连接集群 → 2. 扫描绑定 → 3. 分析权限 → 4. 生成报告
"""

import sys
from k8s_client import get_rbac_api
from scanner import scan_all_bindings
from analyzer import analyze_bindings
from reporter import save_audit_report


def print_banner():
    """打印工具启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════╗
║         🔒 K8s 权限审计小工具 v1.0                    ║
║   Kubernetes RBAC Security Audit Tool               ║
╚══════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """
    主函数：执行完整的审计流程。

    流程步骤：
    1. 打印启动横幅
    2. 连接 Kubernetes 集群
    3. 扫描所有 RoleBinding 和 ClusterRoleBinding
    4. 分析权限绑定，识别风险
    5. 生成 Markdown 格式的审计报告
    6. 输出报告文件路径
    """
    # 步骤 1: 打印启动横幅
    print_banner()

    # 步骤 2: 连接 Kubernetes 集群
    print("[*] 正在连接 Kubernetes 集群...")
    try:
        rbac_api, core_api = get_rbac_api()
    except Exception as e:
        print(f"[✗] 集群连接失败: {e}")
        print("[!] 请确保 kubeconfig 配置正确且集群可访问")
        sys.exit(1)

    # 步骤 3: 扫描所有权限绑定
    print("[*] 正在扫描权限绑定...")
    all_bindings = scan_all_bindings(rbac_api)

    if not all_bindings:
        print("[!] 未发现任何权限绑定，请检查集群状态")
        sys.exit(0)

    # 步骤 4: 分析权限绑定
    print("[*] 正在分析权限风险...")
    audit_results = analyze_bindings(all_bindings)

    # 步骤 5: 生成审计报告
    print("[*] 正在生成审计报告...")
    report_path = save_audit_report(audit_results)

    # 步骤 6: 输出结果摘要
    print("=" * 60)
    print("  ✅ 审计完成！")
    print(f"  📄 报告文件: {report_path}")

    # 统计高风险数量
    high_risk_count = sum(1 for r in audit_results if "🔴" in r["risk_level"])
    if high_risk_count > 0:
        print(f"  ⚠️  发现 {high_risk_count} 个高风险权限绑定，请及时处理！")
    else:
        print("  ✅ 未发现高风险权限绑定，集群权限配置良好！")
    print("=" * 60)


if __name__ == "__main__":
    main()
