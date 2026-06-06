from sqlalchemy.orm import Session
from app.models.domain import ReserveSetting, ReserveBalance, Transaction, RefillQueue, OutageSimulation

def process_payment(db: Session, amount: float):
    balance_record = db.query(ReserveBalance).first()
    settings = db.query(ReserveSetting).first()
    outage = db.query(OutageSimulation).first()
    
    if not balance_record:
        balance_record = ReserveBalance(balance=0.0)
        db.add(balance_record)
        db.commit()
    
    routing = "bank"
    status = "success"
    
    # 1. Use reserve first
    if balance_record.balance >= amount:
        balance_record.balance -= amount
        routing = "reserve"
    else:
        # If reserve insufficient, use bank account
        routing = "bank"
        if outage and outage.is_active:
            status = "failed" # Bank outage active, payment fails if it hits bank
    
    tx = Transaction(amount=amount, status=status, routing=routing)
    db.add(tx)
    db.commit()
    
    # Check auto topup calculations if reserve went below threshold
    if balance_record.balance < settings.threshold:
        queue_refill(db, settings.auto_topup_amount)
    
    return tx

def queue_refill(db: Session, amount: float):
    # Check if a pending refill exists
    existing = db.query(RefillQueue).filter(RefillQueue.status == "pending").first()
    if not existing:
        refill = RefillQueue(amount=amount, status="pending")
        db.add(refill)
        db.commit()

def process_queue(db: Session):
    outage = db.query(OutageSimulation).first()
    if outage and outage.is_active:
        return False # Can't process queue during outage
        
    pending = db.query(RefillQueue).filter(RefillQueue.status == "pending").all()
    balance = db.query(ReserveBalance).first()
    
    for req in pending:
        balance.balance += req.amount
        req.status = "processed"
    
    db.commit()
    return True
