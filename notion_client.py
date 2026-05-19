import requests

from settings import (
    NOTION_TOKEN,
    NOTION_DATABASE_ID,
    NOTION_VERSION,
)


class NotionClient:
    def __init__(self):
        self.base_url = "https://api.notion.com/v1"

        self.headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def build_filter(
        self,
        date=None,
        status="Done",
        project=None,
    ):
        conditions = []

        # Status filter
        if status:
            conditions.append({
                "property": "Status",
                "status": {
                    "equals": status
                }
            })

        # Date filter
        if date:
            conditions.append({
                "property": "Date",
                "date": {
                    "equals": date
                }
            })

        # Project filter
        if project:
            conditions.append({
                "property": "Projects",
                "select": {
                    "equals": project
                }
            })

        # 条件なしの場合
        if not conditions:
            return None

        return {
            "and": conditions
        }

    def query_database(
        self,
        filter_payload=None,
        page_size=100,
    ):
        url = (
            f"{self.base_url}/databases/"
            f"{NOTION_DATABASE_ID}/query"
        )

        all_results = []
        next_cursor = None

        while True:
            payload = {
                "page_size": page_size,
            }

            if filter_payload:
                payload["filter"] = filter_payload

            if next_cursor:
                payload["start_cursor"] = next_cursor

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            all_results.extend(data["results"])

            if not data["has_more"]:
                break

            next_cursor = data["next_cursor"]

        return all_results
