from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.domain import ReserveSetting, ReserveBalance, Transaction, RefillQueue, OutageSimulation
from app.services.engine import process_payment, process_queue
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: float

@router.get("/reserve/balance")
def get_balance(db: Session = Depends(get_db)):
    return db.query(ReserveBalance).first()

@router.get("/reserve/settings")
def get_settings(db: Session = Depends(get_db)):
    return db.query(ReserveSetting).first()

@router.post("/payments")
def create_payment(req: PaymentRequest, db: Session = Depends(get_db)):
    result = process_payment(db, req.amount)
    return result

@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.id.desc()).all()

@router.get("/refill-queue")
def get_queue(db: Session = Depends(get_db)):
    return db.query(RefillQueue).order_by(RefillQueue.id.desc()).all()

@router.post("/refill-queue/process")
def trigger_queue_process(db: Session = Depends(get_db)):
    return {"processed": process_queue(db)}

@router.get("/outage-simulation")
def get_outage(db: Session = Depends(get_db)):
    return db.query(OutageSimulation).first()

@router.post("/outage-simulation/toggle")
def toggle_outage(db: Session = Depends(get_db)):
    outage = db.query(OutageSimulation).first()
    outage.is_active = not outage.is_active
    db.commit()
    db.refresh(outage)
    if not outage.is_active:
        process_queue(db) # Resume ops
    return outage
