def format_summary(
    summary,
    period_label,
):
    lines = []

    lines.append("=== Project Summary ===")
    lines.append(f"Period: {period_label}")
    lines.append("")

    for project, spent in sorted(
        summary["project_totals"].items()
    ):
        lines.append(
            f"{project}  {spent:.2f}h"
        )

    lines.append("--")
    lines.append(
        f"Total  {summary['total_time']:.2f}h"
    )

    lines.append("")
    lines.append("=== Task Details ===")
    lines.append("")

    for project, tasks in sorted(
        summary["project_tasks"].items()
    ):
        lines.append(project)

        for task in tasks:
            lines.append(
                f"- {task['name']}  {task['spent_time']:.2f}h"
            )

        lines.append("")

    return "\n".join(lines)
