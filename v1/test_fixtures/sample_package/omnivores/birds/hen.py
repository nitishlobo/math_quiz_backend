"""Hen."""

from v1.test_fixtures.sample_package.air_animals import AirAnimal
from v1.test_fixtures.sample_package.base import Animal


class Rooster:
    """Rooster."""


class Hen(Animal):
    """Hen."""


class Pullet(AirAnimal):
    """Pullet."""

    class Meta:
        """Properties of a pullet."""

        beak = "short"


def colour(hen: str):
    """Colour."""
    return f"red {hen}"
