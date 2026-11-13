from sqlalchemy import select
from models import User
from security import verify_password

def test_users(client, db_session):
    response = client.post(
        "/users",
        json={
            "email": "example@mail.com",
            "username": "examplename",
            "password": "examplepass",
        },
    )
    assert response.status_code == 201

    user = db_session.scalar(
        select(User).where(User.email == "example@mail.com")
    )
    assert user is not None

    body = response.json()
    assert body["email"] == user.email
    assert body["username"] == user.username
    assert body["id"] == user.id
    assert "password" not in body
    assert "password_hash" not in body
    assert verify_password("examplepass", user.password_hash)