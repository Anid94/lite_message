from psycopg.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import User
from security import hash_password, verify_password, create_access_token
from repo.users import UsersRepo
from schemas import UserCreate, UserLogin, UserUpdate
from exceptions import EmailAlreadyIsTaken, UsernameAlreadyIsTaken, InvalidCredentials, InvalidToken


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

    def login(self, payload: UserLogin) -> str:
        user = self.repo.get_by_email(payload.email)
        if user is None:
            raise InvalidCredentials
        if not verify_password(payload.password, user.password_hash):
            raise InvalidCredentials
        return create_access_token(user.id, user.token_version)

    def update(self, payload: UserUpdate, current_user: User) -> User:
        changes = payload.model_dump(exclude_unset=True)
        if changes == {}:
            return current_user
        if "username" in changes and changes["username"] != current_user.username:
            if self.repo.get_by_username(changes["username"]) is not None:
                raise UsernameAlreadyIsTaken

        try:
            user = self.repo.update(changes, current_user.id)
            if user is None:
                raise InvalidToken()
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError as exc:
            self.db.rollback()
            if isinstance(exc.orig, UniqueViolation):
                const_name = exc.orig.diag.constraint_name
                if const_name == "users_username_key":
                    raise UsernameAlreadyIsTaken() from exc
            raise
        except Exception:
            self.db.rollback()
            raise
        return user