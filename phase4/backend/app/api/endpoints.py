from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from app.db.database import get_db
from app.models.domain import Transaction, UserRisk, SpendingProfile, Recommendation, Insight
from app.services.analytics import run_analytical_pipeline

router = APIRouter()

@router.post("/analytics/user/{user_id}/run")
def trigger_analytics(user_id: str, db: Session = Depends(get_db)):
    return run_analytical_pipeline(db, user_id)

@router.get("/analytics/dashboard/{user_id}")
def get_analytics_dashboard(user_id: str, db: Session = Depends(get_db)):
    profile = db.query(SpendingProfile).filter(SpendingProfile.user_id == user_id).first()
    rec = db.query(Recommendation).filter(Recommendation.user_id == user_id).first()
    risk = db.query(UserRisk).filter(UserRisk.user_id == user_id).first()
    insights = db.query(Insight).filter(Insight.user_id == user_id).all()
    
    return {
        "profile": profile,
        "recommendation": rec,
        "risk": risk,
        "insights": insights
    }

@router.get("/analytics/trends/{user_id}")
def get_spending_trends(user_id: str, db: Session = Depends(get_db)):
    # Group by date for charts
    if db.bind.dialect.name == 'sqlite':
        trends = db.query(
            func.strftime('%Y-%m-%d', Transaction.created_at).label('date'),
            func.sum(Transaction.amount).label('total_amount')
        ).filter(Transaction.user_id == user_id).group_by('date').order_by('date').limit(14).all()
    else: # postgres
        trends = db.query(
            cast(Transaction.created_at, Date).label('date'),
            func.sum(Transaction.amount).label('total_amount')
        ).filter(Transaction.user_id == user_id).group_by(cast(Transaction.created_at, Date)).order_by(cast(Transaction.created_at, Date)).limit(14).all()
        
    return [{"date": str(t.date), "amount": float(t.total_amount) or 0.0} for t in trends]
