"""Ambidextrous."""

from v1.test_fixtures.sample_package.land_animals import LandAnimal
from v1.test_fixtures.sample_package.sea_animals import SeaAnimal


class AmbidextrousAnimal(LandAnimal, SeaAnimal):
    """Ambidextrous."""
