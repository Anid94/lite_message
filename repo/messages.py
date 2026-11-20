from sqlalchemy import select, update, delete, or_, and_
from sqlalchemy.orm import Session, joinedload
from models import Message


class MessagesRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self, sender_id: int, recipient_id: int, text: str
    ) -> Message:
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            text=text,
        )
        self.db.add(message)
        return message

    def get_dialog(
            self, user_a: int, user_b: int, limit: int, before_id: int | None
    ) -> list[Message]:
        stmt = select(Message).where(
            or_(
                and_(
                    Message.sender_id  == user_a,
                    Message.recipient_id == user_b,
                ),
                and_(
                    Message.sender_id == user_b,
                    Message.recipient_id == user_a,
                ),
            )
        )
        if before_id is not None:
            stmt = stmt.where(Message.id < before_id)
        stmt = stmt.order_by(Message.id.desc()).limit(limit)
        return self.db.scalars(stmt).all()