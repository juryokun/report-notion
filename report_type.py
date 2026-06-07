from settings import (
    DAILY_TEMPLATE_ID,
    MONTHLY_TEMPLATE_ID,
    ONDEMAND_TEMPLATE_ID,
    WEEKLY_TEMPLATE_ID,
)

DAILY_REPORT = "DailyReport"
WEEKLY_REPORT = "WeeklyReport"
MONTHLY_REPORT = "MonthlyReport"
QUARTERLY_REPORT = "QuarterlyReport"
SEMIANNUAL_REPORT = "SemiAnnualReport"
ANNUAL_REPORT = "AnnualReport"


def daily_report() -> tuple[str, str]:
    return (
        DAILY_REPORT,
        DAILY_TEMPLATE_ID,
    )


def weekly_report() -> tuple[str, str]:
    return (
        WEEKLY_REPORT,
        WEEKLY_TEMPLATE_ID,
    )


def monthly_report() -> tuple[str, str]:
    return (
        MONTHLY_REPORT,
        MONTHLY_TEMPLATE_ID,
    )


def quarterly_report() -> tuple[str, str]:
    return (
        QUARTERLY_REPORT,
        ONDEMAND_TEMPLATE_ID,
    )


def semiannual_report() -> tuple[str, str]:
    return (
        SEMIANNUAL_REPORT,
        ONDEMAND_TEMPLATE_ID,
    )


def annual_report() -> tuple[str, str]:
    return (
        ANNUAL_REPORT,
        ONDEMAND_TEMPLATE_ID,
    )
