from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from exceptions import CantRequestYourself, ContactAlreadyExists, UserNotFound, ContactNotFound, ContactAlreadyAccepted, \
    ContactNotPending, ContactNotAccepted
from repo.contacts import ContactsRepo
from repo.users import UsersRepo
from models import Contact, User


class ContactService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ContactsRepo(db)
        self.users_repo = UsersRepo(db)

    def create(self, requester_id: int, addressee_id: int) -> Contact:
        if requester_id == addressee_id:
            raise CantRequestYourself
        if self.users_repo.get_by_id(addressee_id) is None:
            raise UserNotFound
        if self.repo.get_contacts_pair(user_a=requester_id, user_b=addressee_id) is not None:
            raise ContactAlreadyExists
        try:
            contact = self.repo.create(requester_id, addressee_id)
            self.db.commit()
            self.db.refresh(contact)
            return contact
        except IntegrityError as exc:
            self.db.rollback()
            if isinstance(exc.orig, UniqueViolation):
                const_name = exc.orig.diag.constraint_name
                if const_name == "uq_contacts_pair":
                    raise ContactAlreadyExists() from exc
            raise
        except Exception:
            self.db.rollback()
            raise

    def get_incoming(self, addressee_id: int) -> list[Contact]:
        return self.repo.get_incoming(addressee_id)

    def get_accepted(self, user_id: int) -> list[User]:
        contacts = self.repo.get_accepted(user_id)
        result = [
            contact.requester
            if contact.addressee_id == user_id
            else contact.addressee
            for contact in contacts
        ]
        return result

    def accept(self, requester_id: int, addressee_id: int) -> Contact:
        if requester_id == addressee_id:
            raise CantRequestYourself
        contact = self.repo.get_contact(requester_id, addressee_id)
        if contact is None:
            raise ContactNotFound
        if contact.status == "accepted":
            raise ContactAlreadyAccepted
        try:
            accepted = self.repo.update(requester_id, addressee_id, {"status": "accepted"})
            if accepted is None:
                raise ContactNotPending
            self.db.commit()
            self.db.refresh(accepted)
        except Exception:
            self.db.rollback()
            raise
        return accepted

    def decline(
            self, requester_id: int, addressee_id: int
    ) -> None:
        contact = self.repo.get_contact(requester_id, addressee_id)
        if contact is None:
            raise ContactNotFound
        if contact.status != "pending":
            raise ContactNotPending
        try:
            rowcount = self.repo.decline(requester_id, addressee_id)
            if rowcount == 0:
                raise ContactNotPending
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def delete(
            self, peer_id: int, user_id: int
    ) -> None:
        contact_pair = self.repo.get_contacts_pair(peer_id, user_id)
        if contact_pair is None:
            raise ContactNotFound
        if contact_pair.status != "accepted":
            raise ContactNotAccepted
        try:
            rowcount = self.repo.delete(contact_pair.requester_id, contact_pair.addressee_id)
            if rowcount == 0:
                raise ContactNotAccepted
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise