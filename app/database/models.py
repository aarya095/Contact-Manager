from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from app.database.database import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str]
    password_hash : Mapped[str] = mapped_column(String(50)) 

class Contact(Base):
    __tablename__ = "contacts"

    contact_id : Mapped[int] = mapped_column(primary_key=True)
    contact_name : Mapped[str] 
    contact_number : Mapped[bytes] 
    onwer_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"))

Base.metadata.create_all(engine)