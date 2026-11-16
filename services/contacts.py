from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from exceptions import CantRequestYourself, ContactAlreadyExists, UserNotFound
from repo.contacts import ContactsRepo
from repo.users import UsersRepo
from models import Contact


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