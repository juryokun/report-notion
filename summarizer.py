from collections import defaultdict


def extract_title(page):
    titles = page["properties"]["Name"]["title"]

    if not titles:
        return "(No Title)"

    return titles[0]["plain_text"]


def extract_project(page):
    project = page["properties"]["ProjectName"]["formula"]

    if not project:
        return "No Project"

    return project["string"]


def extract_spent_time(page):
    value = page["properties"]["Spent Time"]["number"]

    return value or 0.0


def summarize(results):
    project_totals = defaultdict(float)
    project_tasks = defaultdict(list)

    total_time = 0.0

    for page in results:
        project = extract_project(page)
        task_name = extract_title(page)
        spent_time = extract_spent_time(page)

        project_totals[project] += spent_time
        total_time += spent_time

        project_tasks[project].append({
            "name": task_name,
            "spent_time": spent_time,
        })

    return {
        "project_totals": dict(project_totals),
        "project_tasks": dict(project_tasks),
        "total_time": total_time,
    }
