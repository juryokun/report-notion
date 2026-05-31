from typing import Any


def format_project_summary(
    summary: dict[str, Any],
) -> str:
    lines: list[str] = []

    project_totals = summary["project_totals"]

    for project, spent_time in sorted(project_totals.items()):
        lines.append(f"{project}\u3000{spent_time:.2f}h")

    lines.append("--")
    lines.append(
        f"Total\u3000{summary['total_time']:.2f}h"
    )

    return "\n".join(lines)


def format_task_details(
    summary: dict[str, Any],
) -> str:
    lines: list[str] = []

    project_tasks = summary["project_tasks"]

    for project, tasks in sorted(project_tasks.items()):
        lines.append(f"### {project}")
        lines.append("")

        for task in tasks:
            lines.append(
                f"- {task['name']}\u3000"
                f"{task['spent_time']:.2f}h"
            )

        lines.append("")

    return "\n".join(lines)
