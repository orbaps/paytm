from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.domain import ReserveSetting, ReserveBalance, Transaction, RefillQueue, OutageSimulation, AuditEvent, BankHealth, UserRisk
from app.services.engine import process_payment, log_event
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: float
    user_id: str = "user_1"

@router.get("/reserve/balance")
def get_balance(db: Session = Depends(get_db)):
    return db.query(ReserveBalance).first()

@router.get("/reserve/settings")
def get_settings(db: Session = Depends(get_db)):
    return db.query(ReserveSetting).first()

@router.post("/payments")
def create_payment(req: PaymentRequest, db: Session = Depends(get_db)):
    return process_payment(db, req.amount, req.user_id)

@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.id.desc()).all()

@router.get("/refill-queue")
def get_queue(db: Session = Depends(get_db)):
    return db.query(RefillQueue).order_by(RefillQueue.id.desc()).all()

@router.post("/outage/start")
def start_outage(db: Session = Depends(get_db)):
    outage = db.query(OutageSimulation).filter(OutageSimulation.is_active == True).first()
    if not outage:
        outage = OutageSimulation(is_active=True)
        db.add(outage)
        
        bank_health = db.query(BankHealth).filter(BankHealth.bank_id == "bank_1").first()
        if bank_health:
            bank_health.health_score = 0.0
            bank_health.status = "critical"
            
        log_event(db, "outage_detected", "Bank Outage Active")
        db.commit()
    return {"status": "Outage Started"}

@router.post("/outage/end")
def end_outage(db: Session = Depends(get_db)):
    outage = db.query(OutageSimulation).filter(OutageSimulation.is_active == True).first()
    if outage:
        outage.is_active = False
        outage.ended_at = func.now()
        
        bank_health = db.query(BankHealth).filter(BankHealth.bank_id == "bank_1").first()
        if bank_health:
            bank_health.health_score = 100.0
            bank_health.status = "healthy"
            
        log_event(db, "outage_recovered", "Bank Outage Ended")
        db.commit()
    return {"status": "Outage Ended"}

@router.get("/bank-health")
def get_bank_health(db: Session = Depends(get_db)):
    return db.query(BankHealth).all()

@router.get("/user-risk")
def get_user_risk(db: Session = Depends(get_db)):
    return db.query(UserRisk).all()

@router.get("/protected-transactions")
def get_protected_transactions(db: Session = Depends(get_db)):
    count = db.query(Transaction).filter(Transaction.is_protected == True).count()
    return {"protected_count": count}

@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    return db.query(AuditEvent).order_by(AuditEvent.id.desc()).limit(20).all()

@router.get("/outage-status")
def outage_status(db: Session = Depends(get_db)):
    outages = db.query(OutageSimulation).filter(OutageSimulation.is_active == True).all()
    return {"active": len(outages) > 0}
