from fastapi.testclient import TestClient
from app.main import app
from app.db.database import engine, Base, SessionLocal
from app.models.domain import ReserveSetting, ReserveBalance, BankHealth, UserRisk, OutageSimulation

client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(ReserveSetting(target_balance=1000.0, threshold=200.0, auto_topup_amount=500.0))
    db.add(ReserveBalance(balance=400.0))
    db.add(BankHealth(bank_id="bank_1", health_score=100.0, status="healthy"))
    db.add(UserRisk(user_id="user_1", risk_score=10.0, risk_level="low"))
    db.add(UserRisk(user_id="user_bad", risk_score=95.0, risk_level="high"))
    db.commit()
    db.close()

def test_user_risk_blocks_transaction():
    response = client.post("/api/v1/payments", json={"amount": 100.0, "user_id": "user_bad"})
    assert response.status_code == 200
    assert response.json()["routing"] == "blocked"
    assert response.json()["status"] == "failed"

def test_integration_outage_protects_transaction():
    client.post("/api/v1/outage/start")
    
    # Try payment from reserve
    response = client.post("/api/v1/payments", json={"amount": 100.0, "user_id": "user_1"})
    assert response.json()["routing"] == "reserve"
    assert response.json()["is_protected"] == True
    
    # Verify protected transaction counter
    prot = client.get("/api/v1/protected-transactions")
    assert prot.json()["protected_count"] == 1

def test_bank_health_api():
    bh = client.get("/api/v1/bank-health")
    assert len(bh.json()) == 1

def test_events_api():
    events = client.get("/api/v1/events")
    # should be valid list
    assert isinstance(events.json(), list)
