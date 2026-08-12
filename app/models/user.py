# AI helped with imports
from app.db.database import Base
from typing import List
from typing import Any
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column, relationship
from sqlalchemy import func, JSON, String
from sqlalchemy.dialects.mysql import INTEGER
import datetime


# Lead Object - works as a Python Object that represents a SQL table named "lead"
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(11))
    tos_accepted_at: Mapped[datetime.datetime]

    # copied from https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    # Ai helped with JSON column
    user_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable = True)

    lead: Mapped[List["Lead"]] = relationship(back_populates="user")