"""General helper functions and classes."""

from typing import get_type_hints


def get_class_variables(cls: type) -> set[str]:
    """Return set of class field names.

    Keyword args:
    cls -- class or instance of a class
    """
    class_annotations = get_type_hints(cls)
    return set(class_annotations.keys())
