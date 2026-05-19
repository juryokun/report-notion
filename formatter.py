def format_summary(summary):
    lines = []

    project_totals = summary["project_totals"]
    project_tasks = summary["project_tasks"]
    total_time = summary["total_time"]

    # =========================
    # Project Summary
    # =========================

    lines.append("=== Project Summary ===")
    lines.append("")

    for project, spent in sorted(project_totals.items()):
        lines.append(
            f"{project}  {spent:.2f}h"
        )

    lines.append("--")
    lines.append(f"Total  {total_time:.2f}h")

    lines.append("")
    lines.append("=== Task Details ===")
    lines.append("")

    # =========================
    # Task Details
    # =========================

    for project, tasks in sorted(project_tasks.items()):
        lines.append(project)

        for task in tasks:
            lines.append(
                f"- {task['name']}  {task['spent_time']:.2f}h"
            )

        lines.append("")

    return "\n".join(lines)
