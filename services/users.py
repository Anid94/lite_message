from psycopg.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import User
from security import hash_password
from repo.users import UsersRepo
from schemas import UserCreate
from exceptions import EmailAlreadyIsTaken, UsernameAlreadyIsTaken


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsersRepo(db)

    def register(self, payload: UserCreate) -> User:
        if self.repo.get_by_email(payload.email) is not None:
            raise EmailAlreadyIsTaken
        if self.repo.get_by_username(payload.username) is not None:
            raise UsernameAlreadyIsTaken
        password_hash = hash_password(payload.password)
        user = self.repo.create(
            email=payload.email,
            username=payload.username,
            display_name=payload.display_name,
            password_hash=password_hash
        )
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            if isinstance(exc.orig, UniqueViolation):
                const_name = exc.orig.diag.constraint_name
                if const_name == "users_email_key":
                    raise EmailAlreadyIsTaken() from exc
                if const_name == "users_username_key":
                    raise UsernameAlreadyIsTaken() from exc
            raise
        self.db.refresh(user)
        return user
