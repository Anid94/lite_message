import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete, text
from sqlalchemy.orm import Session

from main import app
from database import database_url, get_db
from models import User

test_engine = create_engine(
    database_url.set(database="lite_message_test")
)

@pytest.fixture
def db_session():
    with Session(test_engine) as session:
        database_name = session.scalar(text("SELECT current_database()"))

        if database_name != "lite_message_test":
            raise RuntimeError("Refusing to clean a non-test database")

        session.execute(delete(User))
        session.commit()

        try:
            yield session
        finally:
            session.rollback()
            session.execute(delete(User))
            session.commit()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)