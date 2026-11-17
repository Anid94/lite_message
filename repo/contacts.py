from fastapi import Depends
from sqlalchemy import select, update, delete, or_, and_
from sqlalchemy.orm import Session, joinedload

from models import Contact


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

    def get_incoming(
            self, addressee_id: int
    ) -> list[Contact]:
        stmt = select(Contact).where(
            Contact.addressee_id == addressee_id,
            Contact.status == "pending"
        ).order_by(Contact.id.desc())
        return self.db.scalars(stmt).all()

    def get_accepted(self, user_id: int) -> list[Contact]:
        stmt = select(Contact).where(
            or_(
                Contact.requester_id == user_id,
                Contact.addressee_id == user_id,
            )
        ).where(Contact.status == "accepted").order_by(
            Contact.id.desc()
        ).options(
            joinedload(Contact.requester),
            joinedload(Contact.addressee),
        )
        return self.db.scalars(stmt).all()

    def get_contact(
            self, requester_id: int, addressee_id: int
    ) -> Contact | None:
        stmt = select(Contact).where(
            Contact.requester_id == requester_id,
            Contact.addressee_id == addressee_id,
        )
        return self.db.scalar(stmt)

    def update(
            self,
            requester_id: int,
            addressee_id: int,
            values: dict,
    ) -> Contact | None:
        stmt = update(Contact).where(
            Contact.requester_id == requester_id,
            Contact.addressee_id == addressee_id,
            Contact.status == "pending",
        ).values(values).returning(Contact)
        return self.db.scalar(stmt)


    def decline(
            self, requester_id: int, addressee_id: int
    ) -> int:
        stmt = delete(Contact).where(
            Contact.requester_id == requester_id,
            Contact.addressee_id == addressee_id,
            Contact.status == "pending"
        )
        return self.db.execute(stmt).rowcount

    def delete(
            self,
            requester_id: int,
            addressee_id: int,
    ) -> int:
        stmt = delete(Contact).where(
            Contact.requester_id == requester_id,
            Contact.addressee_id == addressee_id,
            Contact.status == "accepted",
        )
        return self.db.execute(stmt).rowcount
