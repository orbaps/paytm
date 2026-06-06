from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.domain import ReserveSetting, ReserveBalance, Transaction, RefillQueue, OutageSimulation, AuditEvent, BankHealth, UserRisk

def log_event(db: Session, event_type: str, description: str):
    event = AuditEvent(event_type=event_type, description=description)
    db.add(event)
    db.commit()

def calculate_reserve_health(db: Session):
    balance_record = db.query(ReserveBalance).first()
    settings = db.query(ReserveSetting).first()
    if not balance_record or not settings:
        return
    
    old_status = balance_record.health_status
    if balance_record.balance < settings.threshold:
        balance_record.health_status = "critical"
    elif balance_record.balance < settings.target_balance * 0.5:
        balance_record.health_status = "warning"
    else:
        balance_record.health_status = "healthy"
        
    db.commit()
    if old_status != balance_record.health_status:
        log_event(db, "health_update", f"Reserve health changed to {balance_record.health_status}")

def queue_refill(db: Session, amount: float):
    existing = db.query(RefillQueue).filter(RefillQueue.status == "pending").first()
    if not existing:
        refill = RefillQueue(amount=amount, status="pending")
        db.add(refill)
        log_event(db, "auto_topup", f"Queued refill of Rs.{amount}")
        db.commit()

def process_payment(db: Session, amount: float, user_id: str = "user_1"):
    balance_record = db.query(ReserveBalance).first()
    settings = db.query(ReserveSetting).first()
    outages = db.query(OutageSimulation).filter(OutageSimulation.is_active == True).all()
    user_risk = db.query(UserRisk).filter(UserRisk.user_id == user_id).first()
    
    if not balance_record:
        balance_record = ReserveBalance(balance=0.0)
        db.add(balance_record)
        db.commit()
    
    # User risk rule - reject payment if risk level is high
    if user_risk and user_risk.risk_level == "high":
        tx = Transaction(amount=amount, status="failed", routing="blocked", user_id=user_id)
        db.add(tx)
        db.commit()
        log_event(db, "payment_blocked", f"Payment Rs.{amount} blocked due to high user risk {user_id}")
        return tx

    routing = "bank"
    status = "success"
    is_protected = False
    
    # 1. Use reserve first
    if balance_record.balance >= amount:
        balance_record.balance -= amount
        routing = "reserve"
        if len(outages) > 0:
            is_protected = True
    else:
        # Bank account fallback
        routing = "bank"
        if len(outages) > 0:
            status = "failed"
    
    tx = Transaction(amount=amount, status=status, routing=routing, user_id=user_id, is_protected=is_protected)
    db.add(tx)
    db.commit()
    
    if is_protected:
        log_event(db, "protected_transaction", f"Protected payment of Rs.{amount} from reserve during outage")

    # Update Health
    calculate_reserve_health(db)
    
    return tx

def process_queue_worker(db: Session):
    outages = db.query(OutageSimulation).filter(OutageSimulation.is_active == True).all()
    if len(outages) > 0:
        return 0 # Can't process queue during outage
        
    pending = db.query(RefillQueue).filter(RefillQueue.status == "pending").all()
    balance = db.query(ReserveBalance).first()
    
    processed_count = 0
    for req in pending:
        balance.balance += req.amount
        req.status = "processed"
        log_event(db, "queue_processed", f"Processed queued refill of Rs.{req.amount}")
        processed_count += 1
    
    db.commit()
    if processed_count > 0:
        calculate_reserve_health(db)
    return processed_count

def check_thresholds_worker(db: Session):
    balance_record = db.query(ReserveBalance).first()
    settings = db.query(ReserveSetting).first()
    if balance_record and settings:
        if balance_record.balance < settings.threshold:
            queue_refill(db, settings.auto_topup_amount)
