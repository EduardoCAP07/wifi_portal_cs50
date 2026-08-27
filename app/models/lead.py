# AI helped with imports
from app.db.database import Base
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from app.models.user import User

# Lead Object - works as a Python Object that represents a SQL table named "lead"
class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(14))
    email: Mapped[str] = mapped_column(String(254))

    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="lead")
    visits: Mapped[List["Visit"]] = relationship(back_populates="lead")