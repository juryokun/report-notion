from datetime import date, timedelta


def today_range():
    today = date.today()

    return (
        today.isoformat(),
        today.isoformat(),
    )

def yesterday_range():
    today = date.today()
    yesterday = today - timedelta(days=1)

    return (
        yesterday.isoformat(),
        yesterday.isoformat(),
    )


def week_range():
    today = date.today()

    start = today - timedelta(days=today.weekday())

    return (
        start.isoformat(),
        today.isoformat(),
    )

def last_week_range():
    today = date.today()

    this_week_start = (
        today - timedelta(days=today.weekday())
    )

    start = this_week_start - timedelta(days=7)
    end = this_week_start - timedelta(days=1)

    return (
        start.isoformat(),
        end.isoformat(),
    )


def month_range():
    today = date.today()

    start = today.replace(day=1)

    return (
        start.isoformat(),
        today.isoformat(),
    )

def last_month_range():
    today = date.today()

    first_day_this_month = today.replace(day=1)

    last_day_prev_month = (
        first_day_this_month - timedelta(days=1)
    )

    start = last_day_prev_month.replace(day=1)

    return (
        start.isoformat(),
        last_day_prev_month.isoformat(),
    )

