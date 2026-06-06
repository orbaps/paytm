from fastapi.testclient import TestClient
from app.main import app
from app.db.database import engine, Base, SessionLocal
from app.models.domain import ReserveSetting, ReserveBalance, OutageSimulation

client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(ReserveSetting(target_balance=1000.0, threshold=200.0, auto_topup_amount=500.0))
    db.add(ReserveBalance(balance=400.0))
    db.add(OutageSimulation(is_active=False))
    db.commit()
    db.close()

def test_get_balance():
    response = client.get("/api/v1/reserve/balance")
    assert response.status_code == 200
    assert response.json()["balance"] == 400.0

def test_payment_uses_reserve():
    response = client.post("/api/v1/payments", json={"amount": 100.0})
    assert response.status_code == 200
    assert response.json()["routing"] == "reserve"
    
    # Check balance decreased
    balance_resp = client.get("/api/v1/reserve/balance")
    assert balance_resp.json()["balance"] == 300.0

def test_payment_uses_bank_if_reserve_insufficient():
    # Setup initial balance
    response = client.post("/api/v1/payments", json={"amount": 500.0})
    assert response.status_code == 200
    assert response.json()["routing"] == "bank"

def test_auto_topup_queues_on_threshold():
    # balance is 400, threshold is 200. Let's make payment of 300.
    response = client.post("/api/v1/payments", json={"amount": 300.0})
    # Balance is now 100, which is < 200
    queue_resp = client.get("/api/v1/refill-queue")
    assert len(queue_resp.json()) == 1
    assert queue_resp.json()[0]["status"] == "pending"

def test_outage_simulation():
    # Toggle outage
    client.post("/api/v1/outage-simulation/toggle")
    
    # Try payment > reserve
    response = client.post("/api/v1/payments", json={"amount": 500.0})
    assert response.json()["routing"] == "bank"
    assert response.json()["status"] == "failed"
