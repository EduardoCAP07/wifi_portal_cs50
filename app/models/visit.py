# AI helped with imports
from app.db.database import Base
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, JSON, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
import datetime
from app.models.lead import Lead


# Lead Object - works as a Python Object that represents a SQL table named "lead"
class Visit(Base):
    __tablename__ = "visit"
    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    ssid: Mapped[str] = mapped_column(String(100))
    mac: Mapped[str] = mapped_column(String(17))
    tos_accepted_at: Mapped[datetime.datetime]

    # copied from https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    # Ai helped with JSON column
    visit_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable = True)

    lead_id = mapped_column(ForeignKey("leads.id"))

    lead: Mapped[Lead] = relationship(back_populates="visits")