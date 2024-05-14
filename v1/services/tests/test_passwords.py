"""Test common module services."""

import pytest

from v1.services.passwords import hash_password, is_password_correct


@pytest.mark.parametrize(
    "password",
    [("MyPassword37!"), ("=TopSecRET42"), ("^12aErT"), ("0GK$oqZtg5,rXPL*MXxy"), ("$%5{3^pRfNu,E6Fp2vjB")],
)
def test_hash_password(password: str) -> None:
    """Test password hash correctly.

    This test is very rudimentary. Since, we are using a library to hash the password
    """
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert password != hashed_password


matching_password_hashed_list = [
    (
        "MyPassword37!",
        "$argon2id$v=19$m=65536,t=3,p=4$5bKFl+XBcLFRMIsHU0/AsA$qX8Vc96TdHbcwvA79wRE/kodmcMVCCgyWB0dhIHjzgo",
    ),
    (
        "=TopSecRET42",
        "$argon2id$v=19$m=65536,t=3,p=4$ixvAtu9fi/atFBl/HaomFA$bJmQbofpcQoye5/z27Kk6idpfa8L0rtdFF4oNFfRvX4",
    ),
    (
        "^12aErT",
        "$argon2id$v=19$m=65536,t=3,p=4$t3DBH7pcNuktvz6z7m5RBA$WO/YOxJF2xUuWr33ZOmCOXLYTLuFfLr8/0oizaqxibU",
    ),
]


@pytest.mark.parametrize(
    ("password", "hashed_password"),
    matching_password_hashed_list,
    ids=[combo[0] for combo in matching_password_hashed_list],
)
def test_is_password_correct_with_password_which_matches_hashed_password(password: str, hashed_password: str) -> None:
    """Test whether is_correct_password detects a password that matches a hashed passwored correctly."""
    assert is_password_correct(password, hashed_password) is True


mismatching_password_hashed_list = [
    (
        "^0GK$oqZtg5,rXPL*MXxy",
        "$argon2id$v=19$m=65536,t=3,p=4$FP3SXga4+KKEf5dich37oA$JRZHodPVm2RrsmwCiX8o2Cx7FKCQ30XCin52pdcxjrI",
    ),
    (
        "$%5{3^pRfNu,E6Fp2vjB",
        "$argon2id$v=19$m=65536,t=3,p=4$oBW+QnpbSU9QKzUuXHI1Xg$D2aiI9037Lskrp5FWxoPf0+M59R2oYq3+PVw0O53tSE",
    ),
    (
        "#yAm5$*KNA&hZVRx.aS,",
        "notAValidHash",
    ),
]


@pytest.mark.parametrize(
    ("password", "hashed_password"),
    mismatching_password_hashed_list,
    ids=[combo[0] for combo in mismatching_password_hashed_list],
)
def test_is_password_correct_with_password_which_does_not_match_hashed_password(
    password: str,
    hashed_password: str,
) -> None:
    """Test whether is_correct_password detects a password that does not match a hashed passwored correctly."""
    assert is_password_correct(password, hashed_password) is False
