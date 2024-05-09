"""Helper functions for settings."""


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
