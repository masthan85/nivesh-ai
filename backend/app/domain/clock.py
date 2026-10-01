from datetime import datetime, timezone


def utc_now_naive() -> datetime:
    """Current UTC time without tzinfo, matching the existing naive DateTime columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
