from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Outage(Base):
    __tablename__ = "outages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id", ondelete="CASCADE"), index=True, nullable=False)
    outage_type: Mapped[str] = mapped_column(String(80), nullable=False)
    planned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    severity: Mapped[str] = mapped_column(String(40), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(240), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bank = relationship("Bank", back_populates="outages")
