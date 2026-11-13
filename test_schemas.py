import pytest
from pydantic import ValidationError

from schemas import UserCreate

def test_user_create_normalizes_fields():
    user = UserCreate(
        email="Test@test.ru",
        username="Test",
        display_name="Test_name",
        password="test_pass"
    )
    assert user.email == "test@test.ru"
    assert user.username == "test"
    assert user.password == "test_pass"

def test_user_create_rejects_short_username():
    with pytest.raises(ValidationError):
        UserCreate(
            email="Test@test.ru",
            username="Te",
            display_name="Test_name",
            password="test_pass"
        )