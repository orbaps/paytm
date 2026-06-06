from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class ReserveSetting(Base):
    __tablename__ = "reserve_settings"
    id = Column(Integer, primary_key=True, index=True)
    target_balance = Column(Float, default=1000.0)
    threshold = Column(Float, default=200.0)
    auto_topup_amount = Column(Float, default=500.0)

class ReserveBalance(Base):
    __tablename__ = "reserve_balance"
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String)  # success, failed
    routing = Column(String) # reserve, bank
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RefillQueue(Base):
    __tablename__ = "refill_queue"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String, default="pending") # pending, processed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OutageSimulation(Base):
    __tablename__ = "outage_simulation"
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=False)
