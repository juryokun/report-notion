from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Environment variable '{name}' is not set."
        )

    return value


NOTION_TOKEN = _get_env("NOTION_TOKEN")

TASK_DATABASE_ID = _get_env("TASK_DATABASE_ID")
REPORT_DATABASE_ID = _get_env("REPORT_DATABASE_ID")

DAILY_TEMPLATE_ID = _get_env("DAILY_TEMPLATE_ID")
WEEKLY_TEMPLATE_ID = _get_env("WEEKLY_TEMPLATE_ID")
MONTHLY_TEMPLATE_ID = _get_env("MONTHLY_TEMPLATE_ID")
ONDEMAND_TEMPLATE_ID = _get_env("ONDEMAND_TEMPLATE_ID")

NOTION_VERSION = "2022-06-28"
