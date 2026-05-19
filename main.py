import argparse
from datetime import date

from dotenv import load_dotenv

from notion_client import NotionClient
from summarizer import summarize
from formatter import format_summary

# .env 読み込み
load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Target date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--status",
        default="Done",
        help="Status filter"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    notion = NotionClient()

    filter_payload = notion.build_filter(
        date=args.date,
        status=args.status,
    )

    results = notion.query_database(
        filter_payload=filter_payload
    )
    import json

    summary = summarize(results)

    output = format_summary(summary)

    print(output)


if __name__ == "__main__":
    main()
