"""Test for utils."""

from datetime import datetime, timezone

import pytest

from v1.utils.utils import convert_string_to_bool, get_class_variables


@pytest.mark.parametrize("bool_as_str", ["1", "t", "T", "true", "True", "TRUE", "y", "Y", "yes", "Yes", "YES"])
def test_convert_string_to_bool_for_true_cases(bool_as_str: str) -> None:
    """Test convert string to bool for cases where the result should be True."""
    assert convert_string_to_bool(bool_as_str) is True


@pytest.mark.parametrize("bool_as_str", ["0", "f", "F", "false", "False", "FALSE", "n", "N", "no", "No", "NO"])
def test_convert_string_to_bool_for_false_cases(bool_as_str: str) -> None:
    """Test convert string to bool for cases where the result should be False."""
    assert convert_string_to_bool(bool_as_str) is False


def test_get_class_variables_for_regular_class(complex_regular_class: type) -> None:
    """Test get_class_variables function for a regular but complex class as well as it's instance."""
    expected_class_variables = {"created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by"}

    # Verify class variables for a class
    assert get_class_variables(complex_regular_class) == expected_class_variables
    # Verify class variables for an instance of a class
    assert get_class_variables(complex_regular_class(duration=123)) == expected_class_variables


def test_get_class_variables_for_dataclass(complex_dataclass: type) -> None:
    """Test get_class_variables function for a dataclass as well as it's instance."""
    expected_class_variables = {"created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by"}

    # Verify class variables for a class
    assert get_class_variables(complex_dataclass) == expected_class_variables

    # Verify class variables for an instance of a class
    complex_dataclass_instance = complex_dataclass(
        created_at=datetime(2024, 5, 7, 7, 31, 6, 54620, tzinfo=timezone.utc),
        updated_at=datetime(2024, 5, 7, 7, 31, 6, 54620, tzinfo=timezone.utc),
        deleted_at=None,
        created_by="John Jones",
        updated_by="Francis Ngannou",
        deleted_by=None,
    )
    assert get_class_variables(complex_dataclass_instance) == expected_class_variables
