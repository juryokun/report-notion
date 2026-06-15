from typing import Any


def format_project_summary(
    summary: dict[str, Any],
) -> str:
    lines: list[str] = []

    project_totals = summary["project_totals"]

    for project, spent_time in sorted(project_totals.items()):
        spent_time_label = convert_time(spent_time)
        lines.append(f"{project}\u3000{spent_time_label}")

    total_time_label = convert_time(summary["total_time"])
    lines.append("--")
    lines.append(f"Total\u3000{total_time_label}")

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
            spent_time_label = convert_time(task["spent_time"])
            lines.append(f"- {task['name']}\u3000{spent_time_label}")

        lines.append("")

    return "\n".join(lines)


def convert_time(minute: int) -> str:
    result_hour, result_minute = divmod(minute, 60)
    return f"{result_hour}h {result_minute:02}m"
