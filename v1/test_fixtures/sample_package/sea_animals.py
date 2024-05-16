"""Sea creatures."""

from v1.test_fixtures.sample_package.base import Animal


class SeaAnimal(Animal):
    """Mammal."""


class Whale(SeaAnimal):
    """Whale."""


class BlueWhale(Whale):
    """Blue whale."""


class Dolphin(Animal):
    """Dolphin."""
