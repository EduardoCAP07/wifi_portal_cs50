# AI helped with imports
from app.db.database import Base
from typing import Any
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column, relationship
from sqlalchemy import func, JSON, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from app.models.user import User
import datetime

# Lead Object - works as a Python Object that represents a SQL table named "lead"
class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(14))
    email: Mapped[str] = mapped_column(String(254))
    ssid: Mapped[str] = mapped_column(String(100))
    mac: Mapped[str] = mapped_column(String(17))
    tos_accepted_at: Mapped[datetime.datetime]

    # copied from https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    # Ai helped with JSON column
    lead_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable = True)

    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="lead")