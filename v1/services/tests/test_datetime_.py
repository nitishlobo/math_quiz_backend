"""Test datetime services."""

from datetime import datetime, timedelta, timezone

import pytest

from v1.services.datetime_ import validate_datetime_is_utc_timezone


@pytest.mark.parametrize(
    "datetime_obj",
    [datetime.now(timezone.utc), datetime(2021, 4, 28, 13, 1, 23, 34567, tzinfo=timezone.utc)],
)
def test_validate_datetime_is_utc_timezone(datetime_obj: datetime) -> None:
    """Test datetime validator for UTC timezone returns correctly."""
    validated_datetime_obj = validate_datetime_is_utc_timezone(datetime_obj)
    assert validated_datetime_obj == datetime_obj


@pytest.mark.parametrize(
    "datetime_obj",
    [
        datetime(2024, 5, 21),  # noqa: DTZ001
        datetime(2024, 5, 21, 12, 3, 1),  # noqa: DTZ001
        datetime(2024, 5, 21, 12, 3, 4, tzinfo=timezone(timedelta(hours=5, minutes=30))),
        datetime(2024, 5, 21, 12, 3, 4, tzinfo=timezone(timedelta(hours=-6))),
        datetime(2024, 5, 21, 12, 3, 4, tzinfo=timezone(timedelta(hours=10))),
    ],
    ids=[
        "date-only",
        "naive-datetime",
        "ist-datetime",  # Bangalore - Indian Standard Time
        "mdt-datetime",  # El Paso - Mountain Daylight Time
        "aest-datetime",  # Brisbane - Australian Eastern Standard Time
    ],
)
def test_validate_datetime_is_utc_timezone_with_non_utc_timezones(datetime_obj: datetime) -> None:
    """Test datetime validator for UTC timezone returns correctly."""
    with pytest.raises(ValueError, match="Datetime object does not have a UTC timezone."):
        validate_datetime_is_utc_timezone(datetime_obj)
