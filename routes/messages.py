from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Message, User
from schemas import MessageRead, MessageCreate
from services.messages import MessageService
from dependencies import get_current_user



router = APIRouter(prefix="/messages", tags=["messages"])

def get_message_service(
        db: Session = Depends(get_db)
) -> MessageService:
    return MessageService(db)


@router.get("/dialog_with/{other_user}", status_code=200, response_model=list[MessageRead])
def get_dialog(
        other_user: int,
        limit: int = Query(default=30, ge=1, le=100),
        before_id: int | None = Query(default=None, gt=0),
        current_user: User = Depends(get_current_user),
        service: MessageService = Depends(get_message_service),
):
    return service.get_dialog(
        user_a=current_user.id,
        user_b=other_user,
        limit=limit,
        before_id=before_id,
    )


@router.post("/{recipient_id}", status_code=201, response_model=MessageRead)
def send_message(
        recipient_id: int,
        payload: MessageCreate,
        current_user: User = Depends(get_current_user),
        service: MessageService = Depends(get_message_service)
):
    return service.create_message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        text=payload.text,
    )