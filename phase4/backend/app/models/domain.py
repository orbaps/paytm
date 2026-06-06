from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.db.database import Base
from datetime import datetime

class ReserveSetting(Base):
    __tablename__ = "reserve_settings"
    id = Column(Integer, primary_key=True, index=True)
    target_balance = Column(Float, default=1000.0)
    threshold = Column(Float, default=200.0)
    auto_topup_amount = Column(Float, default=500.0)

class ReserveBalance(Base):
    __tablename__ = "reserve_balance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="user_1")
    balance = Column(Float, default=0.0)
    health_status = Column(String, default="healthy")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String)  # success, failed
    routing = Column(String) # reserve, bank
    user_id = Column(String, default="user_1")
    is_protected = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

class RefillQueue(Base):
    __tablename__ = "refill_queue"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String, default="pending") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OutageSimulation(Base):
    __tablename__ = "outage_simulation"
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=False)
    bank_id = Column(String, default="bank_1")

class BankHealth(Base):
    __tablename__ = "bank_health"
    id = Column(Integer, primary_key=True, index=True)
    bank_id = Column(String)
    health_score = Column(Float, default=100.0)
    status = Column(String, default="healthy")

# --- PHASE 4 MODELS ---

class UserRisk(Base):
    __tablename__ = "user_risk"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    risk_score = Column(Float, default=0.0) 
    risk_level = Column(String, default="low") 
    factors = Column(JSON, default=list) # Explainable factors
    last_calculated = Column(DateTime(timezone=True), default=func.now())

class SpendingProfile(Base):
    __tablename__ = "spending_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    avg_daily_spend = Column(Float, default=0.0)
    recent_velocity = Column(Float, default=0.0) # spend in last 3 days
    profile_type = Column(String, default="Standard")
    last_calculated = Column(DateTime(timezone=True), default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    recommended_reserve = Column(Float, default=0.0)
    gap = Column(Float, default=0.0)
    explanation = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Insight(Base):
    __tablename__ = "insights"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    content = Column(String)
    insight_type = Column(String) # e.g., 'spending_trend', 'risk_alert'
    created_at = Column(DateTime(timezone=True), default=func.now())
