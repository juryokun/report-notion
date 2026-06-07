import argparse
import logging
import sys

from clipboard import copy_to_clipboard
from date_range import (
    last_month_range,
    last_week_range,
    month_range,
    today_range,
    week_range,
    yesterday_range,
)
from formatter import (
    format_project_summary,
    format_task_details,
)
from notion_client import NotionClient
from report_type import (
    annual_report,
    daily_report,
    monthly_report,
    quarterly_report,
    semiannual_report,
    weekly_report,
)
from summarizer import summarize

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Notion work reports.")

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--today",
        action="store_true",
        help="Today",
    )

    group.add_argument(
        "--yesterday",
        action="store_true",
        help="Yesterday",
    )

    group.add_argument(
        "--week",
        action="store_true",
        help="Current week",
    )

    group.add_argument(
        "--last-week",
        action="store_true",
        help="Previous week",
    )

    group.add_argument(
        "--month",
        action="store_true",
        help="Current month",
    )

    group.add_argument(
        "--last-month",
        action="store_true",
        help="Previous month",
    )

    parser.add_argument(
        "--report-type",
        choices=["daily", "weekly", "monthly", "quarterly", "semiannual", "annual"],
        help="daily/weekly/monthly/quarterly/semiannual/annual",
    )

    parser.add_argument(
        "--to-date",
        help="YYYY-MM-DD",
    )

    parser.add_argument(
        "--from-date",
        help="YYYY-MM-DD",
    )

    parser.add_argument(
        "--display",
        action="store_true",
        help="Display Only",
    )

    return parser.parse_args()


def resolve_args(
    args: argparse.Namespace,
) -> tuple[tuple[str, str, str], tuple[str, str]]:
    if args.from_date or args.to_date:
        if not args.from_date:
            raise ValueError("--from-date is required")
        if not args.to_date:
            raise ValueError("--to-date is required")
        if not args.report_type:
            raise ValueError("--report_type is required")

        if args.report_type == "daily":
            report_type, template_id = daily_report()
        elif args.report_type == "weekly":
            report_type, template_id = weekly_report()
        elif args.report_type == "monthly":
            report_type, template_id = monthly_report()
        elif args.report_type == "quarterly":
            report_type, template_id = quarterly_report()
        elif args.report_type == "semiannual":
            report_type, template_id = semiannual_report()
        else:
            report_type, template_id = annual_report()

        return (
            (args.from_date, args.to_date, f"{args.from_date} ~ {args.to_date}"),
            (report_type, template_id),
        )
    else:
        if args.yesterday:
            return (
                yesterday_range(),
                daily_report(),
            )
        if args.week:
            return (
                week_range(),
                weekly_report(),
            )
        if args.last_week:
            return (
                last_week_range(),
                weekly_report(),
            )
        if args.month:
            return (
                month_range(),
                monthly_report(),
            )
        if args.last_month:
            return (
                last_month_range(),
                monthly_report(),
            )

        return (
            today_range(),
            daily_report(),
        )


def main() -> int:
    configure_logging()

    try:
        args = parse_args()

        register_mode = True
        if args.display:
            register_mode = False

        (start_date, end_date, report_name), (report_type, template_id) = resolve_args(
            args
        )

        logger.info(
            "Target period: %s - %s",
            start_date,
            end_date,
        )

        notion = NotionClient()

        tasks = notion.query_tasks(
            start_date=start_date,
            end_date=end_date,
        )

        logger.info(
            "Fetched %s tasks",
            len(tasks),
        )

        summary = summarize(tasks)

        project_summary = format_project_summary(summary)

        task_details = format_task_details(summary)

        if register_mode:
            notion.upsert_report(
                report_name=report_name,
                report_type=report_type,
                template_id=template_id,
                project_summary=project_summary,
                start_date=start_date,
                end_date=end_date,
            )

            copy_to_clipboard(task_details)

            print()
            print("========================================")
            print("Report updated successfully")
            print("========================================")
            print()

            print(f"Report Name : {report_name}")
            print(f"Period      : {start_date} ~ {end_date}")
            print()

            print(project_summary)

            print()
            print("Task details copied to clipboard.")
            print()

        else:
            print()
            print("========================================")
            print("Report")
            print("========================================")
            print()

            print(f"Report Name : {report_name}")
            print(f"Period      : {start_date} ~ {end_date}")
            print()

            print(project_summary)

            print()
            print("========================================")
            print("Task List")
            print("========================================")
            print()
            print(task_details)

        return 0

    except Exception as exc:
        logger.exception("Unexpected error")

        print()
        print("ERROR")
        print("-----")
        print(str(exc))
        print()

        return 1


if __name__ == "__main__":
    sys.exit(main())
