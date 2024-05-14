"""Common factory related functionality."""

import factory


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory functionality."""

    class Meta:
        """Factory boy metadata."""

        abstract = True
