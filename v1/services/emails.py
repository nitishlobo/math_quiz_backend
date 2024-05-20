"""Email related services."""

from email_validator import validate_email


def validate_and_normalize_email(email: str, *, check_deliverability: bool = True) -> str:
    """Return a normalised email if email is a valid email.

    Raise the following error from email_validator.
    EmailNotValidError - if the form of the address is invalid or if the domain name fails DNS checks

    Keyword arguments:
    email -- email needed to be validated
    check_deliverability -- checks ability to send an email to the address.
        Set it to False to avoid unnecessary DNS queries (default True)
    """
    email_info = validate_email(email, check_deliverability=check_deliverability)
    return email_info.normalized
