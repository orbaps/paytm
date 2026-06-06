from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard import DashboardSummary, DashboardTrends
from app.services.analytics import get_dashboard_summary, get_dashboard_trends


router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)


@router.get("/trends", response_model=DashboardTrends)
def dashboard_trends(db: Session = Depends(get_db)):
    return get_dashboard_trends(db)
