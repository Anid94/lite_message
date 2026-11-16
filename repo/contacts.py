from fastapi import Depends
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from models import Contact
from schemas import ContactRead


class ContactsRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_contacts_pair(
            self, user_a: int, user_b: int
    ) -> Contact | None:
        stmt = select(Contact).where(
            or_(
                and_(
                    Contact.requester_id == user_a,
                    Contact.addressee_id == user_b,
                ),
                and_(
                    Contact.requester_id == user_b,
                    Contact.addressee_id == user_a,
                )
            )
        )
        return self.db.scalar(stmt)

    def create(
            self, requester_id: int, addressee_id: int
    ) -> Contact:
        contact = Contact(
            requester_id=requester_id,
            addressee_id=addressee_id,
        )
        self.db.add(contact)
        return contact

    def get_incoming(self, addressee_id: int) -> list[Contact]:
        stmt = select(Contact).where(
            Contact.addressee_id == addressee_id,
            Contact.status == "pending"
        ).order_by(Contact.id.desc())
        return self.db.scalars(stmt).all()