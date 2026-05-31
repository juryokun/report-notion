import argparse

from notion_client import NotionClient
from summarizer import summarize
from formatter import format_summary

from date_range import (
    today_range,
    yesterday_range,
    week_range,
    last_week_range,
    month_range,
    last_month_range,
)


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--today",
        action="store_true",
        help="Today's report",
    )

    group.add_argument(
        "--yesterday",
        action="store_true",
        help="Yesterday's report",
    )

    group.add_argument(
        "--week",
        action="store_true",
        help="This week's report",
    )

    group.add_argument(
        "--last-week",
        action="store_true",
        help="Last week's report",
    )

    group.add_argument(
        "--month",
        action="store_true",
        help="This month's report",
    )

    group.add_argument(
        "--last-month",
        action="store_true",
        help="Last month's report",
    )

    parser.add_argument(
        "--from-date",
        help="YYYY-MM-DD",
    )

    parser.add_argument(
        "--to-date",
        help="YYYY-MM-DD",
    )

    parser.add_argument(
        "--project",
        help="Project filter",
    )

    return parser.parse_args()

def resolve_period(args):
    # 任意期間
    if args.from_date or args.to_date:
        if not args.from_date:
            raise ValueError(
                "--from-date is required"
            )

        if not args.to_date:
            raise ValueError(
                "--to-date is required"
            )

        return (
            args.from_date,
            args.to_date,
            f"{args.from_date} ~ {args.to_date}",
        )

    # 固定オプション
    if args.week:
        start, end = week_range()

    elif args.last_week:
        start, end = last_week_range()

    elif args.month:
        start, end = month_range()

    elif args.last_month:
        start, end = last_month_range()
    elif args.yesterday:
        start, end = yesterday_range()

    else:
        start, end = today_range()

    return (
        start,
        end,
        f"{start} ~ {end}",
    )

def main():
    args = parse_args()

    start_date, end_date, period_label = (
        resolve_period(args)
    )

    notion = NotionClient()

    filter_payload = notion.build_filter(
        from_date=start_date,
        to_date=end_date,
        status="Done",
        project=args.project,
    )

    results = notion.query_database(
        filter_payload
    )

    summary = summarize(results)

    output = format_summary(
        summary,
        period_label,
    )

    print(output)


if __name__ == "__main__":
    main()
