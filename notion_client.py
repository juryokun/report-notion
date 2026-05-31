import logging
from typing import Any

import requests

from settings import (
    NOTION_TOKEN,
    NOTION_VERSION,
    REPORT_DATABASE_ID,
    TASK_DATABASE_ID,
)


logger = logging.getLogger(__name__)


class NotionClient:
    def __init__(self) -> None:
        self.base_url = "https://api.notion.com/v1"

        self.headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    #
    # Common
    #

    def _post(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as exc:
            logger.exception("Notion API POST failed")
            raise RuntimeError(
                f"Failed to call Notion API: {exc}"
            ) from exc

    def _patch(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = requests.patch(
                url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as exc:
            logger.exception("Notion API PATCH failed")
            raise RuntimeError(
                f"Failed to call Notion API: {exc}"
            ) from exc

    #
    # Task DB
    #

    def query_tasks(
        self,
        start_date: str,
        end_date: str,
        status: str = "Done",
    ) -> list[dict[str, Any]]:
        """
        Task DBから条件に一致するタスクを取得する。
        """

        url = f"{self.base_url}/databases/{TASK_DATABASE_ID}/query"

        filter_payload = {
            "and": [
                {
                    "property": "Status",
                    "status": {
                        "equals": status,
                    },
                },
                {
                    "property": "Date",
                    "date": {
                        "on_or_after": start_date,
                    },
                },
                {
                    "property": "Date",
                    "date": {
                        "on_or_before": end_date,
                    },
                },
            ]
        }

        results: list[dict[str, Any]] = []
        next_cursor: str | None = None

        while True:
            payload: dict[str, Any] = {
                "filter": filter_payload,
                "page_size": 100,
            }

            if next_cursor:
                payload["start_cursor"] = next_cursor

            data = self._post(url, payload)

            results.extend(data["results"])

            if not data["has_more"]:
                break

            next_cursor = data["next_cursor"]

        logger.info(
            "Fetched %s tasks (%s - %s)",
            len(results),
            start_date,
            end_date,
        )

        return results

    #
    # Report DB
    #

    def find_report_by_name(
        self,
        report_name: str,
    ) -> str | None:
        """
        Report DBからNameでレポートを検索する。
        """

        url = f"{self.base_url}/databases/{REPORT_DATABASE_ID}/query"

        payload = {
            "filter": {
                "property": "Name",
                "title": {
                    "equals": report_name,
                },
            }
        }

        data = self._post(url, payload)

        results = data["results"]

        if not results:
            return None

        return results[0]["id"]

    def create_report(
        self,
        report_name: str,
        report_type: str,
        template_id: str,
        project_summary: str,
        start_date: str,
        end_date: str,
    ) -> None:
        """
        Reportページを新規作成する。
        """

        url = f"{self.base_url}/pages"

        date_property = {
            "start": start_date,
        }

        if start_date != end_date:
            date_property["end"] = end_date

        payload = {
            "parent": {
                "database_id": REPORT_DATABASE_ID,
            },
            "template": {
                "type": "template_id",
                "template_id": template_id,
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": report_name,
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": report_type,
                    }
                },
                "ProjectsSummary": {
                    "rich_text": [
                        {
                            "text": {
                                "content": project_summary,
                            }
                        }
                    ]
                },
                "Date": {
                    "date": date_property,
                },
            },
        }

        self._post(url, payload)

        logger.info("Created report: %s", report_name)

    def update_report(
        self,
        page_id: str,
        report_type: str,
        project_summary: str,
        start_date: str,
        end_date: str,
    ) -> None:
        """
        Reportページを更新する。
        """

        url = f"{self.base_url}/pages/{page_id}"

        date_property = {
            "start": start_date,
        }

        if start_date != end_date:
            date_property["end"] = end_date

        payload = {
            "properties": {
                "ProjectsSummary": {
                    "rich_text": [
                        {
                            "text": {
                                "content": project_summary,
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": report_type,
                    }
                },
                "Date": {
                    "date": date_property,
                },
            }
        }

        self._patch(url, payload)

        logger.info("Updated report: %s", page_id)

    def upsert_report(
        self,
        report_name: str,
        report_type: str,
        template_id: str,
        project_summary: str,
        start_date: str,
        end_date: str,
    ) -> None:
        """
        Nameで検索し、存在すれば更新、
        存在しなければ新規作成する。
        """

        page_id = self.find_report_by_name(report_name)

        if page_id:
            self.update_report(
                page_id=page_id,
                report_type=report_type,
                project_summary=project_summary,
                start_date=start_date,
                end_date=end_date,
            )
            return

        self.create_report(
            report_name=report_name,
            report_type=report_type,
            template_id=template_id,
            project_summary=project_summary,
            start_date=start_date,
            end_date=end_date,
        )
