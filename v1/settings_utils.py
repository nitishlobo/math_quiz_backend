"""Helper functions for settings."""


def convert_string_to_bool(bool_as_str: str) -> bool:
    """Convert a string representing a boolean to a boolean type."""
    return bool_as_str.lower() in ["true", "t", "yes", "y", "1"]
