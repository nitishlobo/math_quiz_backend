"""Helper functions for settings."""

import importlib
import inspect
import pkgutil


def convert_string_to_bool(bool_as_str: str) -> bool:
    """Convert a string representing a boolean to a boolean type."""
    return bool_as_str.lower() in ["true", "t", "yes", "y", "1"]


def get_class_variables(cls_or_instance: type | object) -> set[str]:
    """Return a set of attribute names that are considered to be class-level variables that are not private.

    Include attributes defined in the class body and type hints for dataclasses.
    Exclude any private variables defined by a single or double underscore.

    Keyword args:
    cls_or_instance -- class or instance to inspect
    """
    class_vars = set()

    # Analyse the class only, not an instance of the class
    cls = cls_or_instance if isinstance(cls_or_instance, type) else type(cls_or_instance)

    for name, value in cls.__dict__.items():
        # Filter out dunder methods, functions and class methods
        if not name.startswith("__") and not callable(value) and not isinstance(value, classmethod):
            class_vars.add(name)

    # Include the fields from the __annotations__ if present (especially useful for dataclasses)
    if hasattr(cls, "__annotations__"):
        class_vars.update(cls.__annotations__.keys())

    # Exclude private variables
    return {class_var for class_var in class_vars if not class_var.startswith("_")}


def get_classes_from_package_recursively(package: str) -> list[type]:
    """Return a list of classes inside a given package (recurse thorugh any sub-packages).

    Keyword arguments:
    package -- package represented as a string. Must not be relative.

    Example:
    >>> classes = get_classes_from_package_recursively(package="v1.database.models")
    >>> classes
    ... [SqlAlchemyBase, TimeAudit, Users, etc...]
    """
    classes_in_package = []
    # Go through the modules in the package
    for _importer, module_name, is_package in pkgutil.iter_modules(importlib.import_module(package).__path__):
        full_module_name = f"{package}.{module_name}"
        # Recurse through any sub-packages
        if is_package:
            classes_in_subpackage = get_classes_from_package_recursively(package=full_module_name)
            classes_in_package.extend(classes_in_subpackage)

        # Load the module for inspection
        module = importlib.import_module(full_module_name)

        # Iterate through all the objects in the module and
        # using the lambda, filter for class objects and only objects that exist within the module
        for _name, obj in inspect.getmembers(
            module,
            lambda member, module_name=full_module_name: inspect.isclass(member) and member.__module__ == module_name,
        ):
            classes_in_package.append(obj)
    return classes_in_package


def get_subclasses_of_class_from_package_recursively(parent_class: type, package: str) -> list[type]:
    """Return a list of subclasses (i.e. classes which inherit from the parent_class) inside a given package.

    This will work recursively for any package.

    Keyword arguments:
    parent_class -- parent class from which the subclasses need to be found
    package -- package which needs to be searched for subclasses. Must not be relative.

    Example:
    >>> from v1.database.models.base import SqlAlchemyBase
    >>> alchemy_models = get_subclasses_of_class_from_package(parent_class=SqlAlchemyBase, package="v1.database.models")
    >>> alchemy_models
    ... [Users, etc...]
    """
    classes_in_package = get_classes_from_package_recursively(package)
    return [class_ for class_ in classes_in_package if issubclass(class_, parent_class) and class_ is not parent_class]
