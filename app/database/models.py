# Built-in Modules
from typing import List

# User-Defined Modules
from app.database.database import engine

# External Modules
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(
        unique = True,
        index = True,
    )
    password_hash : Mapped[str] = mapped_column(String(255)) 
    contacts : Mapped[List["Contact"]] = relationship(back_populates = "owner")

class Contact(Base):
    __tablename__ = "contacts"

    contact_id : Mapped[int] = mapped_column(primary_key=True)
    contact_name : Mapped[str] 
    contact_number : Mapped[bytes] 
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    owner : Mapped["User"] = relationship(back_populates = "contacts")

Base.metadata.create_all(engine)