from sqlalchemy.orm import Session
from exceptions import UserNotFound, ContactNotAccepted, ContactNotFound

from models import Message
from repo.messages import MessagesRepo
from repo.users import UsersRepo
from repo.contacts import ContactsRepo


class MessageService:
    def __init__(self,db: Session):
        self.db = db
        self.messages_repo = MessagesRepo(db)
        self.users_repo = UsersRepo(db)
        self.contacts_repo = ContactsRepo(db)

    def get_dialog(
            self, user_a: int,
            user_b: int,
            limit: int,
            before_id: int | None,
    ) -> list[Message]:
        if user_a != user_b:
            contact = self.contacts_repo.get_contacts_pair(user_a, user_b)
            if contact is None:
                raise ContactNotFound
            if contact.status != "accepted":
                raise ContactNotAccepted
        dialog = self.messages_repo.get_dialog(user_a, user_b, limit, before_id)
        return dialog

    def create_message(
            self, sender_id: int, recipient_id: int, text: str
    ) -> Message:
        user = self.users_repo.get_by_id(recipient_id)
        if user is None or user.deleted_at is not None:
            raise UserNotFound
        if sender_id != recipient_id:
            contact = self.contacts_repo.get_contacts_pair(sender_id, recipient_id)
            if contact is None:
                raise ContactNotFound
            if contact.status != "accepted":
                raise ContactNotAccepted
        try:
            message = self.messages_repo.create(
                sender_id, recipient_id, text
            )
            self.db.commit()
            self.db.refresh(message)
        except Exception:
            self.db.rollback()
            raise
        return message
