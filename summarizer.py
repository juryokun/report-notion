from collections import defaultdict
from typing import Any


def extract_title(page: dict[str, Any]) -> str:
    try:
        title = page["properties"]["Name"]["title"]

        if not title:
            return "(No Title)"

        return title[0]["plain_text"]

    except (KeyError, IndexError, TypeError):
        return "(No Title)"


def extract_project(page: dict[str, Any]) -> str:
    try:
        project = page["properties"]["ProjectName"]["formula"]["string"]

        return project or "No Project"

    except (KeyError, TypeError):
        return "No Project"


def extract_spent_time(page: dict[str, Any]) -> float:
    try:
        value = page["properties"]["Spent Time"]["number"]

        return float(value or 0)

    except (KeyError, TypeError, ValueError):
        return 0.0


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    project_totals: dict[str, float] = defaultdict(float)
    project_tasks: dict[str, list[dict[str, Any]]] = defaultdict(list)

    total_time = 0.0

    for page in results:
        project = extract_project(page)
        task_name = extract_title(page)
        spent_time = extract_spent_time(page)

        project_totals[project] += spent_time
        total_time += spent_time

        project_tasks[project].append(
            {
                "name": task_name,
                "spent_time": spent_time,
            }
        )

    return {
        "project_totals": dict(project_totals),
        "project_tasks": dict(project_tasks),
        "total_time": total_time,
    }
