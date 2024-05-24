from datetime import datetime, timezone, timedelta


def now() -> datetime:
    return datetime.now(timezone.utc)


def date_round_seconds(dt: datetime, round_down: bool = False):
    if round_down:
        return dt.replace(microsecond=0)
    else:
        newDateTime = dt + timedelta(seconds=.5)
        return newDateTime.replace(microsecond=0)
