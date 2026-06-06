from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class NPCIStatistic(Base):
    __tablename__ = "npci_statistics"
    __table_args__ = (UniqueConstraint("bank_id", "month", "year", name="uq_npci_statistics_bank_month_year"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id", ondelete="CASCADE"), index=True, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    success_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    technical_decline: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    business_decline: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    source: Mapped[str] = mapped_column(String(240), nullable=False, default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bank = relationship("Bank", back_populates="npci_statistics")
