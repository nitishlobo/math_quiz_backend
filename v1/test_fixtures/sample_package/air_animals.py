"""Air animals."""

from v1.test_fixtures.sample_package.base import Animal


class AirAnimal(Animal):
    """Air animal."""

    def flight_speed(self):
        """Return speed of animal."""
        return 32
