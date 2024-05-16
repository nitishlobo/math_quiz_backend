"""Test for utils."""

from collections import Counter
from datetime import datetime, timezone

import pytest

from v1.test_fixtures.sample_package.air_animals import AirAnimal
from v1.test_fixtures.sample_package.ambidextrous import AmbidextrousAnimal
from v1.test_fixtures.sample_package.base import Animal, Helicopter
from v1.test_fixtures.sample_package.land_animals import LandAnimal
from v1.test_fixtures.sample_package.omnivores.bears import BlackBear, PolarBear
from v1.test_fixtures.sample_package.omnivores.birds.hen import Hen, Pullet, Rooster
from v1.test_fixtures.sample_package.omnivores.birds.peacock import African, Indian
from v1.test_fixtures.sample_package.sea_animals import BlueWhale, Dolphin, SeaAnimal, Whale
from v1.utils.utils import (
    convert_string_to_bool,
    get_class_variables,
    get_classes_from_package_recursively,
    get_subclasses_of_class_from_package_recursively,
)


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


@pytest.mark.parametrize(
    ("package", "expected_classes"),
    [
        (
            "v1.test_fixtures.sample_package",
            {
                Rooster,
                Hen,
                Pullet,
                Indian,
                African,
                BlackBear,
                PolarBear,
                AirAnimal,
                AmbidextrousAnimal,
                Animal,
                Helicopter,
                LandAnimal,
                SeaAnimal,
                Whale,
                BlueWhale,
                Dolphin,
            },
        ),
        (
            "v1.test_fixtures.sample_package.omnivores",
            {Rooster, Hen, Pullet, Indian, African, BlackBear, PolarBear},
        ),
        (
            "v1.test_fixtures.sample_package.omnivores.birds",
            {Rooster, Hen, Pullet, Indian, African},
        ),
    ],
    ids=[
        "highest-package-level",
        "middle-package-level",
        "lowest-package-level",
    ],
)
def test_get_classes_from_package_recursively(package: str, expected_classes: set[type]) -> None:
    """Test getting all the subclasses belonging to a class from a package."""
    classes = get_classes_from_package_recursively(package)
    assert set(classes) == set(expected_classes)


@pytest.mark.parametrize(
    ("parent_class", "package", "expected_subclasses"),
    [
        (
            Animal,
            "v1.test_fixtures.sample_package",
            [
                AmbidextrousAnimal,
                LandAnimal,
                SeaAnimal,
                Whale,
                BlueWhale,
                Dolphin,
                AirAnimal,
                BlackBear,
                PolarBear,
                Hen,
                Pullet,
            ],
        ),
        (
            Animal,
            "v1.test_fixtures.sample_package.omnivores",
            [BlackBear, PolarBear, Hen, Pullet],
        ),
        (
            Animal,
            "v1.test_fixtures.sample_package.omnivores.birds",
            [Hen, Pullet],
        ),
        (
            LandAnimal,
            "v1.test_fixtures.sample_package",
            [AmbidextrousAnimal, PolarBear],
        ),
        (
            LandAnimal,
            "v1.test_fixtures.sample_package.omnivores",
            [PolarBear],
        ),
        (
            LandAnimal,
            "v1.test_fixtures.sample_package.omnivores.birds",
            [],
        ),
        (
            BlueWhale,
            "v1.test_fixtures.sample_package",
            [],
        ),
        (
            BlueWhale,
            "v1.test_fixtures.sample_package.omnivores",
            [],
        ),
        (
            BlueWhale,
            "v1.test_fixtures.sample_package.omnivores.birds",
            [],
        ),
    ],
    ids=[
        "highest-class-order-at-highest-package-level",
        "highest-class-order-at-middle-package-level",
        "lowest-class-order-at-lowest-package-level",
        "middle-class-order-at-highest-package-level",
        "middle-class-order-at-middle-package-level",
        "middle-class-order-at-lowest-package-level",
        "lowest-class-order-at-highest-package-level",
        "lowest-class-order-at-middle-package-level",
        "lowest-class-order-at-lowest-package-level",
    ],
)
def test_get_subclasses_of_class_from_package_recursively(
    parent_class: type,
    package: str,
    expected_subclasses: list[type],
) -> None:
    """Test getting all the subclasses belonging to a class from a package."""
    animal_subclasses = get_subclasses_of_class_from_package_recursively(parent_class, package)
    assert Counter(animal_subclasses) == Counter(expected_subclasses)
