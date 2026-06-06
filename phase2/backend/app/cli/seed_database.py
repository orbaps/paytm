from app.db.database import SessionLocal, Base, engine
from app.models.domain import ReserveSetting, ReserveBalance, OutageSimulation

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if not db.query(ReserveSetting).first():
        db.add(ReserveSetting(target_balance=2000.0, threshold=500.0, auto_topup_amount=1500.0))
    if not db.query(ReserveBalance).first():
        db.add(ReserveBalance(balance=2000.0))
    if not db.query(OutageSimulation).first():
        db.add(OutageSimulation(is_active=False))
        
    db.commit()
    print("Database seeded!")

if __name__ == "__main__":
    seed_db()
