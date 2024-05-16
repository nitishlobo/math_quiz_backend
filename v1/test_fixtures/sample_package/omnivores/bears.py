"""Bear omnivore creatures."""

from v1.test_fixtures.sample_package.base import Animal
from v1.test_fixtures.sample_package.land_animals import LandAnimal


class BlackBear(Animal):
    """Black bear."""


class PolarBear(LandAnimal):
    """Polar bear."""

    @classmethod
    def get_defence_power(cls) -> int:
        """Get ability to defend."""
        return 100
