from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import User
from schemas import ContactRead
from services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags = ["contacts"])

def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(db)


@router.get("/incoming", status_code=200, response_model=list[ContactRead])
def get_incoming(
        current_user: User = Depends(get_current_user),
        service: ContactService = Depends(get_contact_service),
):
    return service.get_incoming(current_user.id)


@router.post("/{addressee_id}", status_code=201, response_model=ContactRead)
def create(
        addressee_id: int,
        service: ContactService = Depends(get_contact_service),
        current_user: User = Depends(get_current_user),
):
    return service.create(
        requester_id=current_user.id,
        addressee_id=addressee_id,
    )