import hashlib
import secrets
from functools import wraps


def hash_password(password):
    """Return a salted hash of a password."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 200000
    ).hex()
    return f"{salt}${password_hash}"


def verify_password(password, saved_hash):
    """Check a password against its saved hash."""
    try:
        salt, expected_hash = saved_hash.split("$", 1)
    except ValueError:
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 200000
    ).hex()

    return secrets.compare_digest(actual_hash, expected_hash)


def requires_login(function):
    """Allow a function to run only for a logged-in user."""
    @wraps(function)
    def wrapper(current_user, *args, **kwargs):
        if current_user is None:
            raise PermissionError("Please log in first")
        return function(current_user, *args, **kwargs)

    return wrapper


def requires_role(role):
    """Allow a function to run only for a specific role."""
    def decorator(function):
        @wraps(function)
        def wrapper(current_user, *args, **kwargs):
            if current_user is None:
                raise PermissionError("Please log in first")
            if current_user.role != role:
                raise PermissionError("You do not have permission")
            return function(current_user, *args, **kwargs)
        return wrapper
    return decorator