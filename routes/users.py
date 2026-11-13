from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserRead, UserCreate
from services.users import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_user_services(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("", status_code=201, response_model=UserRead)
def create_user(
        payload: UserCreate,
        service: UserService = Depends(get_user_services),
):
      return service.register(payload)