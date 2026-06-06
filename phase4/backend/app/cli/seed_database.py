from app.db.database import SessionLocal, Base, engine
from app.models.domain import Transaction, ReserveBalance
from app.services.analytics import run_analytical_pipeline
from datetime import datetime, timedelta
import random

def seed_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Base Reserve balance
    db.add(ReserveBalance(user_id="user_1", balance=1500.0, health_status="healthy"))
    
    # 2. Historical transactions for user_1 (Generating 14 days of data)
    now = datetime.utcnow()
    for day in range(14, -1, -1):
        # 1-3 transactions per day
        daily_txs_count = random.randint(1, 3)
        for _ in range(daily_txs_count):
            amount = random.uniform(50.0, 300.0)
            tx = Transaction(
                amount=amount, 
                status="success", 
                routing="reserve", 
                user_id="user_1",
                created_at=now - timedelta(days=day, hours=random.randint(1, 23))
            )
            db.add(tx)
            
    # Add a burst spend recently to trigger that profile
    burst1 = Transaction(amount=1800.0, status="success", routing="bank", user_id="user_1", created_at=now - timedelta(hours=2))
    burst2 = Transaction(amount=1200.0, status="success", routing="bank", user_id="user_1", created_at=now - timedelta(hours=5))
    db.add(burst1)
    db.add(burst2)
    
    db.commit()
    
    # 3. Run Pipeline so models exist
    run_analytical_pipeline(db, "user_1")
    print("Phase 4 Database seeded with rich historical data and analytics models created!")

if __name__ == "__main__":
    seed_db()
