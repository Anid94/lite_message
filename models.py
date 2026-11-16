from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    token_version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    sent_contacts: Mapped[list["Contact"]] = relationship(
        foreign_keys="Contact.requester_id",
        back_populates="requester",
    )
    received_contacts: Mapped[list["Contact"]] = relationship(
        foreign_keys="Contact.addressee_id",
        back_populates="addressee",
    )


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requester_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    addressee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(8), server_default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    requester: Mapped["User"] = relationship(
        foreign_keys="Contact.requester_id",
        back_populates="sent_contacts",
    )
    addressee: Mapped["User"] = relationship(
        foreign_keys="Contact.addressee_id",
        back_populates="received_contacts",
    )
