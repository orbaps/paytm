from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Bank(Base):
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bank_name: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    bank_type: Mapped[str] = mapped_column(String(80), nullable=False)
    upi_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    outages = relationship("Outage", back_populates="bank", cascade="all, delete-orphan")
    maintenance_notices = relationship("MaintenanceNotice", back_populates="bank", cascade="all, delete-orphan")
    npci_statistics = relationship("NPCIStatistic", back_populates="bank", cascade="all, delete-orphan")
