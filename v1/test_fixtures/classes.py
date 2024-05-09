"""Test fixtures returning classes."""

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, Self

import pytest
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime


@pytest.fixture()
def complex_regular_class():
    """Return a class that has a nested class, instance, class, static and private methods."""

    # pylint: disable=missing-class-docstring, missing-function-docstring
    class ColumnTypes:
        datetime_tz = Annotated[datetime, mapped_column(DateTime(timezone=True))]

    class TimeAudit:
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
        updated_at: Mapped[ColumnTypes.datetime_tz]
        deleted_at: Mapped[ColumnTypes.datetime_tz | None]
        created_by: str
        updated_by: str = "John"
        deleted_by = "Tom"
        _approved_by = "Leigh"
        __mangled_internal_stamp = 123

        class Meta:
            indexed: bool
            table_suffix: str = "_audit"
            trigger = "updated_at"

        def __init__(self: Self, duration: int) -> None:
            self.duration = duration

        def instance_method(self: Self, depth: int, time: int) -> int:
            internal_factors = self._internal_func() * self.__mangled_internal_func() * self.__mangled_internal_stamp
            return internal_factors * depth * time

        @classmethod
        def class_func(cls: type, first_name: str, last_name: str) -> str:
            return f"{first_name} {last_name}"

        @staticmethod
        def static_func(lemons: int, apples: int) -> int:
            return lemons * apples

        def _internal_func(self: Self) -> int:
            return 42

        def __mangled_internal_func(self: Self) -> int:
            return 97

    # pylint: enable=missing-class-docstring, missing-function-docstring

    return TimeAudit


@pytest.fixture()
def complex_dataclass():
    """Return a dataclass that has a nested class, instance, class, static and private methods."""

    # pylint: disable=missing-class-docstring, missing-function-docstring
    class ColumnTypes:
        datetime_tz = Annotated[datetime, mapped_column(DateTime(timezone=True))]

    @dataclass
    class TimeAudit:
        updated_at: Mapped[ColumnTypes.datetime_tz]
        deleted_at: Mapped[ColumnTypes.datetime_tz | None]
        created_by: str
        created_at: datetime
        updated_by: str = "John"
        deleted_by: Any = None
        _approved_by: str = "Leigh"
        __mangled_internal_stamp = 123

        class Meta:
            indexed: bool
            table_suffix: str = "_audit"
            trigger = "updated_at"

        def instance_method(self: Self, depth: int, time: int) -> int:
            internal_factors = self._internal_func() * self.__mangled_internal_func() * self.__mangled_internal_stamp
            return internal_factors * depth * time

        @classmethod
        def class_func(cls: type, first_name: str, last_name: str) -> str:
            return f"{first_name} {last_name}"

        @staticmethod
        def static_func(lemons: int, apples: int) -> int:
            return lemons * apples

        def _internal_func(self: Self) -> int:
            return 42

        def __mangled_internal_func(self: Self) -> int:
            return 97

    # pylint: enable=missing-class-docstring, missing-function-docstring

    return TimeAudit
