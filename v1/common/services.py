"""Services shared across the project."""
from argon2 import PasswordHasher


def hash_password(password: str) -> str:
    """Return hashed password."""
    return PasswordHasher().hash(password)


def is_password_correct(password: str, hashed_password: str) -> bool:
    """Return True if plain text password matches hashed password.

    Raises:
    argon2.exceptions.VerifyMismatchError
        -- raised if verification fails because hash is not valid for password
    argon2.exceptions.VerificationError
        -- raised if verification fails for other reasons
    argon2.exceptions.InvalidHashError
        -- raised if hash is so clearly invalid, that it couldn't be passed to Argon2
    """
    return PasswordHasher().verify(hashed_password, password)
