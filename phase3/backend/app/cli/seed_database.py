from app.db.database import SessionLocal, Base, engine
from app.models.domain import ReserveSetting, ReserveBalance, OutageSimulation, BankHealth, UserRisk

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if not db.query(ReserveSetting).first():
        db.add(ReserveSetting(target_balance=3000.0, threshold=1000.0, auto_topup_amount=2000.0))
    if not db.query(ReserveBalance).first():
        db.add(ReserveBalance(balance=3000.0, health_status="healthy"))
    if not db.query(BankHealth).first():
        db.add(BankHealth(bank_id="bank_1", health_score=100.0, status="healthy"))
    if not db.query(UserRisk).first():
        db.add(UserRisk(user_id="user_1", risk_score=10.0, risk_level="low"))
        db.add(UserRisk(user_id="user_bad", risk_score=95.0, risk_level="high"))
        
    db.commit()
    print("Phase 3 Database seeded!")

if __name__ == "__main__":
    seed_db()
