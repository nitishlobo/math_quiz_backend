"""Datetime services."""

from datetime import datetime, timezone


def validate_datetime_is_utc_timezone(datetime_obj: datetime) -> datetime:
    """Return datetime if datetime has a timezone and is in UTC.

    Raise ValueError if datetime does not have a timezone or is not in UTC.
    """
    if datetime_obj.tzinfo == timezone.utc or datetime_obj.strftime("%Z") == "UTC":
        return datetime_obj

    error_msg = "Datetime object does not have a UTC timezone."
    raise ValueError(error_msg)
