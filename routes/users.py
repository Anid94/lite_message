from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from schemas import UserRead, UserCreate, TokenRead, UserLogin
from services.users import UserService
from models import User

router = APIRouter(prefix="/users", tags=["users"])


def get_user_services(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("/me", status_code=200, response_model=UserRead)
def get_user(
        user: User = Depends(get_current_user)
) -> UserRead:
    return user

@router.post("", status_code=201, response_model=UserRead)
def create_user(
        payload: UserCreate,
        service: UserService = Depends(get_user_services),
):
      return service.register(payload)


@router.post("/login", status_code=200, response_model=TokenRead)
def login(
        payload: UserLogin,
        service: UserService = Depends(get_user_services),
):
    token = service.login(payload)
    return TokenRead(access_token=token)