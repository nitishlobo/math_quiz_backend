"""General helper functions and classes."""


def get_class_variables(cls: type) -> set[str]:
    """Return set of class variables."""
    # Get class attributes
    attributes = vars(cls)

    # Filter out methods, nested classes and dunder (__) attributes
    return {key for key, value in attributes.items() if not callable(value) and not key.startswith("__")}
