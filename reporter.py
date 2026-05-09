"""
K8s 安全审计报告生成器模块
==========================
负责将分析结果格式化为 Markdown 表格，
并输出到项目根目录下的 audit_report.md 文件中。
"""

from typing import List, Dict
from datetime import datetime


# 报告输出路径（项目根目录）
REPORT_FILE_PATH = "audit_report.md"


def generate_report(audit_results: List[Dict]) -> str:
    """
    生成完整的 Markdown 格式审计报告。

    报告包含以下部分：
    1. 报告头部信息（标题、生成时间、集群信息等）
    2. 风险统计摘要
    3. 高风险条目表格（🔴）
    4. 中风险条目表格（🟡）
    5. 低风险条目表格（🟢）
    6. 报告尾部（建议和说明）

    Args:
        audit_results: analyze_bindings() 返回的审计结果列表

    Returns:
        str: 完整的 Markdown 报告内容
    """
    # 统计各类风险的数量
    high_risk = [r for r in audit_results if "🔴" in r["risk_level"]]
    medium_risk = [r for r in audit_results if "🟡" in r["risk_level"]]
    low_risk = [r for r in audit_results if "🟢" in r["risk_level"]]

    # 获取当前时间作为报告生成时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ========== 构建报告内容 ==========
    report_lines = []

    # ---- 1. 报告头部 ----
    report_lines.append("# 🔒 Kubernetes 集群安全审计报告")
    report_lines.append("")
    report_lines.append("## 📋 报告概览")
    report_lines.append("")
    report_lines.append(f"- **报告生成时间**: {now}")
    report_lines.append(f"- **审计工具**: K8s 权限审计小工具 v1.0")
    report_lines.append(f"- **审计范围**: 所有 RoleBinding 和 ClusterRoleBinding")
    report_lines.append(f"- **审计对象**: 所有 ServiceAccount 的权限绑定")
    report_lines.append("")

    # ---- 2. 风险统计摘要 ----
    report_lines.append("## 📊 风险统计摘要")
    report_lines.append("")
    report_lines.append("| 风险等级 | 数量 | 说明 |")
    report_lines.append("|---------|------|------|")
    report_lines.append(
        f"| 🔴 高风险 | {len(high_risk)} | "
        f"非系统 ServiceAccount 绑定了高风险角色（如 cluster-admin） |"
    )
    report_lines.append(
        f"| 🟡 中风险 | {len(medium_risk)} | "
        f"系统 ServiceAccount 绑定了高风险角色（需确认必要性） |"
    )
    report_lines.append(
        f"| 🟢 低风险 | {len(low_risk)} | "
        f"ServiceAccount 绑定了普通角色，权限在合理范围内 |"
    )
    report_lines.append(f"| **总计** | **{len(audit_results)}** | 所有 ServiceAccount 绑定总数 |")
    report_lines.append("")

    # ---- 3. 高风险条目表格 ----
    report_lines.append("## 🔴 高风险条目")
    report_lines.append("")
    report_lines.append(
        "> ⚠️ 以下 ServiceAccount 绑定了高风险角色，"
        "且不属于系统 Namespace，建议立即审查并降低权限。"
    )
    report_lines.append("")

    if high_risk:
        report_lines.append("| 名称空间 | 绑定名称 | 绑定类型 | 角色名称 | ServiceAccount | 风险等级 | 说明 |")
        report_lines.append("|---------|---------|---------|---------|---------------|---------|------|")
        for item in high_risk:
            report_lines.append(
                f"| {item['namespace']} "
                f"| {item['binding_name']} "
                f"| {item['binding_type']} "
                f"| {item['role_name']} "
                f"| {item['sa_namespace']}/{item['sa_name']} "
                f"| {item['risk_level']} "
                f"| {item['description']} |"
            )
    else:
        report_lines.append("*✅ 未发现高风险条目，集群权限配置良好！*")
    report_lines.append("")

    # ---- 4. 中风险条目表格 ----
    report_lines.append("## 🟡 中风险条目")
    report_lines.append("")
    report_lines.append(
        "> ℹ️ 以下系统 ServiceAccount 绑定了高风险角色，"
        "通常是集群组件正常运行所需，建议确认其必要性。"
    )
    report_lines.append("")

    if medium_risk:
        report_lines.append("| 名称空间 | 绑定名称 | 绑定类型 | 角色名称 | ServiceAccount | 风险等级 | 说明 |")
        report_lines.append("|---------|---------|---------|---------|---------------|---------|------|")
        for item in medium_risk:
            report_lines.append(
                f"| {item['namespace']} "
                f"| {item['binding_name']} "
                f"| {item['binding_type']} "
                f"| {item['role_name']} "
                f"| {item['sa_namespace']}/{item['sa_name']} "
                f"| {item['risk_level']} "
                f"| {item['description']} |"
            )
    else:
        report_lines.append("*✅ 未发现中风险条目。*")
    report_lines.append("")

    # ---- 5. 低风险条目表格 ----
    report_lines.append("## 🟢 低风险条目")
    report_lines.append("")
    report_lines.append(
        "> ✅ 以下 ServiceAccount 的权限绑定在合理范围内，"
        "属于正常使用场景。"
    )
    report_lines.append("")

    if low_risk:
        report_lines.append("| 名称空间 | 绑定名称 | 绑定类型 | 角色名称 | ServiceAccount | 风险等级 | 说明 |")
        report_lines.append("|---------|---------|---------|---------|---------------|---------|------|")
        for item in low_risk:
            report_lines.append(
                f"| {item['namespace']} "
                f"| {item['binding_name']} "
                f"| {item['binding_type']} "
                f"| {item['role_name']} "
                f"| {item['sa_namespace']}/{item['sa_name']} "
                f"| {item['risk_level']} "
                f"| {item['description']} |"
            )
    else:
        report_lines.append("*未发现低风险条目。*")
    report_lines.append("")

    # ---- 6. 报告尾部 ----
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## 💡 安全建议")
    report_lines.append("")
    report_lines.append("1. **最小权限原则**: 始终遵循最小权限原则，只授予 ServiceAccount 完成任务所需的最小权限。")
    report_lines.append("2. **定期审计**: 建议定期运行此审计工具，及时发现并处理权限过大问题。")
    report_lines.append("3. **使用自定义角色**: 避免直接绑定 cluster-admin 等高权限角色，应创建自定义角色并授予必要权限。")
    report_lines.append("4. **监控异常绑定**: 关注非系统 Namespace 中出现的高风险角色绑定，这可能是安全事件的征兆。")
    report_lines.append("5. **及时清理**: 删除不再使用的 ServiceAccount 和 RoleBinding，减少攻击面。")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append(f"*报告由 K8s 权限审计小工具自动生成于 {now}*")

    return "\n".join(report_lines)


def write_report_to_file(report_content: str) -> str:
    """
    将报告内容写入文件。

    Args:
        report_content: generate_report() 返回的 Markdown 报告内容

    Returns:
        str: 写入的文件路径
    """
    try:
        with open(REPORT_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"[✓] 审计报告已生成: {REPORT_FILE_PATH}")
        return REPORT_FILE_PATH
    except Exception as e:
        print(f"[✗] 写入报告文件失败: {e}")
        return ""


def save_audit_report(audit_results: List[Dict]) -> str:
    """
    生成并保存审计报告的便捷函数。

    这是报告模块的统一入口，调用此函数即可完成报告的生成和保存。

    Args:
        audit_results: analyze_bindings() 返回的审计结果列表

    Returns:
        str: 报告文件的路径，如果失败则返回空字符串
    """
    print("\n" + "="*60)
    print("  生成审计报告")
    print("="*60)

    # 生成报告内容
    report_content = generate_report(audit_results)

    # 写入文件
    file_path = write_report_to_file(report_content)

    if file_path:
        print(f"  📄 报告文件: {file_path}")
    print("="*60 + "\n")

    return file_path
