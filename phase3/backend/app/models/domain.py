from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
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
    health_status = Column(String, default="healthy") # healthy, warning, critical

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String)  # success, failed
    routing = Column(String) # reserve, bank
    user_id = Column(String, default="user_1")
    is_protected = Column(Boolean, default=False)
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
    bank_id = Column(String, default="bank_1")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String) # auto_topup, outage_detected, queue_processed, payment
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BankHealth(Base):
    __tablename__ = "bank_health"
    id = Column(Integer, primary_key=True, index=True)
    bank_id = Column(String)
    health_score = Column(Float, default=100.0) # 0 to 100
    status = Column(String, default="healthy")

class UserRisk(Base):
    __tablename__ = "user_risk"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    risk_score = Column(Float, default=0.0) # 0 to 100
    risk_level = Column(String, default="low") # low, medium, high
