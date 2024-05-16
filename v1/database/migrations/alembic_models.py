"""This file contains all the SQL alchemy models so that alembic can autogenerate the code for the migrations.

The import for SqlAlchemyBase from this file is then used in env.py so that all the models in this file get
loaded first. This allows alembic to know all the models it needs to autogenerate migration code for.
The alembic command for this is:
alembic revision --autogenerate -m "some message"

Refer to the following for more information:
https://stackoverflow.com/a/15668175/5702056
https://stackoverflow.com/a/70890339/5702056
"""

# pylint: disable=unused-import
from v1.database.models.base import SqlAlchemyBase
from v1.utils.utils import get_subclasses_of_class_from_package_recursively

# Import all the SQL Alchemy models inheriting from SqlAlchemyBase
get_subclasses_of_class_from_package_recursively(parent_class=SqlAlchemyBase, package="v1.database.models")
