import pytest

from models.user import User
from utils.auth import hash_password, verify_password


def test_user_inherits_person_details():
    user = User(
        1, "Test User", "test@example.com",
        hash_password("testpass123"), "borrower"
    )

    assert user.name == "Test User"
    assert user.email == "test@example.com"


def test_password_hash_verifies_correct_password():
    saved_hash = hash_password("testpass123")

    assert verify_password("testpass123", saved_hash) is True
    assert verify_password("wrongpass", saved_hash) is False


def test_user_rejects_invalid_role():
    user = User(
        1, "Test User", "test@example.com",
        hash_password("testpass123"), "borrower"
    )

    with pytest.raises(ValueError):
        user.role = "manager"