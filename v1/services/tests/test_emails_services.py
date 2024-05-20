"""Test email services."""

import pytest
from email_validator import EmailNotValidError, EmailSyntaxError, EmailUndeliverableError

from v1.services.emails import validate_and_normalize_email


@pytest.mark.parametrize(
    "email",
    [
        "egb21321@gmail.com",
        "Abc.123@test-example.com",
        "johnson.david@yahoo.com",
        "jack.sparrow.42b9ab320e0740abbdf991ac1e1ec37f@tru-test.com",
    ],
)
def test_validate_and_normalize_email_with_valid_emails(email: str) -> None:
    """Test validating emails with valid emails."""
    normalized_email = validate_and_normalize_email(email)
    assert normalized_email == email


@pytest.mark.parametrize(
    "email",
    [
        "Abc@example.tld",
        "user+mailbox/department=shipping@example.tld",
        "!#$%&'*+-/=?^_`.{|}~@example.tld",
    ],
)
def test_validate_and_normalize_email_with_undeliverable_emails(email: str) -> None:
    """Test validating emails with emails that have the correct syntax but are not deliverable.

    EmailUndeliverableError is a subclass of EmailNotValidError, so check that error is also generated.
    """
    with pytest.raises(EmailNotValidError):
        validate_and_normalize_email(email, check_deliverability=True)

    with pytest.raises(EmailUndeliverableError):
        validate_and_normalize_email(email, check_deliverability=True)


@pytest.mark.parametrize(
    "email",
    [
        "my@twodots..com",
        "me@-leadingdash",
        ".leadingdot@domain.com",
        "me@trailingdashfw-",
        "me@trailingdashfw－",  # noqa: RUF001
        "чебурашкаящик-с-апельсинами.рф@.com",  # noqa: RUF001
        "उदाहरण..परीक्ष@yahoo.com",
        "jeff葉臺網中/\\心@messenger.com",
    ],
)
def test_validate_and_normalize_email_with_invalid_emails(email: str) -> None:
    """Test validating emails with emails that have the correct syntax but are not deliverable.

    EmailSyntaxError is a subclass of EmailNotValidError, so check that error is also generated.
    """
    with pytest.raises(EmailNotValidError):
        validate_and_normalize_email(email, check_deliverability=True)

    with pytest.raises(EmailSyntaxError):
        validate_and_normalize_email(email, check_deliverability=True)
