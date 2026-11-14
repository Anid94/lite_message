from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import get_db
from exceptions import InvalidToken
from repo.users import UsersRepo
from security import decode_access_token
from models import User


bearer = HTTPBearer(auto_error=False)

def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
        session: Session = Depends(get_db)
) -> User:
    if credentials is None:
        raise InvalidToken
    payload = decode_access_token(credentials.credentials)
    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError) as exc:
        raise InvalidToken from exc

    user = UsersRepo(session).get_by_id(user_id)
    if user is None:
        raise InvalidToken

    token_version = payload["token_version"]
    if type(token_version) is not int or token_version != user.token_version:
        raise InvalidToken
    return user