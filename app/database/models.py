from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from typing import List

from app.database.database import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str]
    password_hash : Mapped[str] = mapped_column(String(50)) 
    contacts : Mapped[List["Contact"]] = relationship(back_populates = "owner")

class Contact(Base):
    __tablename__ = "contacts"

    contact_id : Mapped[int] = mapped_column(primary_key=True)
    contact_name : Mapped[str] 
    contact_number : Mapped[bytes] 
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    owner : Mapped["User"] = relationship(back_populates = "contacts")

Base.metadata.create_all(engine)