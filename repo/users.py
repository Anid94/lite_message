from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


class UsersRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalar(stmt)

    def create(
            self,
            email: str,
            username: str,
            display_name: str | None,
            password_hash: str,
    ) -> User:
        user = User(
            email=email,
            username=username,
            display_name=display_name,
            password_hash=password_hash,
        )
        self.db.add(user)
        return user