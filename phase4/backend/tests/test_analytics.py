from fastapi.testclient import TestClient
from app.main import app
from app.db.database import engine, Base, SessionLocal
from app.models.domain import Transaction, ReserveBalance, SpendingProfile, Recommendation, UserRisk, Insight
from app.services.analytics import run_analytical_pipeline
from datetime import datetime, timedelta

client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(ReserveBalance(user_id="test_user", balance=100.0))
    
    # Create test transactions
    now = datetime.utcnow()
    db.add(Transaction(user_id="test_user", amount=2000.0, created_at=now - timedelta(hours=1)))
    db.add(Transaction(user_id="test_user", amount=150.0, created_at=now - timedelta(days=5)))
    db.commit()
    db.close()

def test_pipeline_execution():
    db = SessionLocal()
    res = run_analytical_pipeline(db, "test_user")
    
    assert res["profile"].user_id == "test_user"
    assert res["profile"].profile_type == "Burst Spender" # due to the big random 2k tx
    
    assert res["recommendation"].gap > 0 # balance is 100
    
    assert res["risk"].risk_level == "high" # burst spreader + high gap
    assert len(res["risk"].factors) > 0
    
    insights = db.query(Insight).filter(Insight.user_id == "test_user").all()
    assert len(insights) > 0

def test_dashboard_api():
    db = SessionLocal()
    run_analytical_pipeline(db, "test_user")
    
    response = client.get("/api/v1/analytics/dashboard/test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["profile_type"] == "Burst Spender"
    assert "insights" in data
