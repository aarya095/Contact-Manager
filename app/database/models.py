from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.database.database import engine

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"

    contact_id : Mapped[int] = mapped_column(primary_key=True)
    contact_name : Mapped[str] 
    contact_number : Mapped[bytes] 

if __name__ == '__main__':
    Base.metadata.create_all(engine)