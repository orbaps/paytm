from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.domain import Transaction, ReserveBalance, UserRisk, SpendingProfile, Recommendation, Insight
import json

def analyze_user_spending(db: Session, user_id: str):
    # 1. Spending Analyzer (Rule-based)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    
    txs_30d = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.created_at >= thirty_days_ago).all()
    txs_3d = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.created_at >= three_days_ago).all()
    
    total_30d = sum(t.amount for t in txs_30d)
    total_3d = sum(t.amount for t in txs_3d)
    
    avg_daily = total_30d / 30 if txs_30d else 0.0
    
    profile_type = "Standard"
    if avg_daily > 1000:
        profile_type = "High Spender"
    elif total_3d > total_30d * 0.4 and total_30d > 0:
        profile_type = "Burst Spender"
        
    profile = db.query(SpendingProfile).filter(SpendingProfile.user_id == user_id).first()
    if not profile:
        profile = SpendingProfile(user_id=user_id)
        db.add(profile)
        
    profile.avg_daily_spend = avg_daily
    profile.recent_velocity = total_3d
    profile.profile_type = profile_type
    profile.last_calculated = datetime.utcnow()
    
    db.commit()
    return profile

def generate_recommendation(db: Session, user_id: str, profile: SpendingProfile):
    # 2. Reserve Recommendation Engine (Explainable Rules)
    # Rule: Recommended = 5 days of avg daily spend + 20% buffer
    recommended_amount = (profile.avg_daily_spend * 5) * 1.2
    recommended_amount = max(recommended_amount, 500.0) # Base minimum
    
    balance_record = db.query(ReserveBalance).filter(ReserveBalance.user_id == user_id).first()
    current_balance = balance_record.balance if balance_record else 0.0
    gap = recommended_amount - current_balance
    
    explanation = f"Based on your avg daily spend of Rs.{profile.avg_daily_spend:.0f}, we recommend a reserve of Rs.{recommended_amount:.0f} to comfortably cover 5 days of transactions."
    
    rec = db.query(Recommendation).filter(Recommendation.user_id == user_id).first()
    if not rec:
        rec = Recommendation(user_id=user_id)
        db.add(rec)
        
    rec.recommended_reserve = recommended_amount
    rec.gap = max(0, gap)
    rec.explanation = explanation
    rec.created_at = datetime.utcnow()
    
    db.commit()
    return rec

def calculate_personalized_risk(db: Session, user_id: str, profile: SpendingProfile, rec: Recommendation):
    # 3. Personalized Risk Engine (Explainable factors)
    base_score = 10.0
    factors = []
    
    # Factor A: High recent velocity
    if profile.recent_velocity > (profile.avg_daily_spend * 4):
        base_score += 30.0
        factors.append("High recent transaction velocity detected (+30 risk).")
        
    # Factor B: Reserve Gap
    if rec.gap > (rec.recommended_reserve * 0.5):
        base_score += 40.0
        factors.append("Current reserve is critically below recommended safe levels (+40 risk).")
        
    # Factor C: Profile Type
    if profile.profile_type == "Burst Spender":
        base_score += 15.0
        factors.append("Categorized as burst spender; prone to sudden large transactions (+15 risk).")
        
    risk_level = "low"
    if base_score > 60:
        risk_level = "high"
    elif base_score > 30:
        risk_level = "medium"
        
    risk = db.query(UserRisk).filter(UserRisk.user_id == user_id).first()
    if not risk:
        risk = UserRisk(user_id=user_id)
        db.add(risk)
        
    risk.risk_score = min(base_score, 100.0)
    risk.risk_level = risk_level
    risk.factors = factors
    risk.last_calculated = datetime.utcnow()
    
    db.commit()
    return risk

def generate_insights(db: Session, user_id: str, profile: SpendingProfile, gap: float):
    # 4. Insight Generator
    db.query(Insight).filter(Insight.user_id == user_id).delete() # refresh insights
    
    insights = []
    if profile.profile_type == "Burst Spender":
        insights.append(Insight(user_id=user_id, insight_type="spending_trend", content="You have occasional bursts of high spending. Consider a higher reserve buffer."))
    else:
        insights.append(Insight(user_id=user_id, insight_type="spending_trend", content=f"Your spending is stable, averaging Rs.{profile.avg_daily_spend:.0f}/day."))
        
    if gap > 0:
        insights.append(Insight(user_id=user_id, insight_type="reserve_alert", content=f"You are Rs.{gap:.0f} short of your recommended reserve. A top-up is advised to stay protected during outages."))
        
    db.add_all(insights)
    db.commit()

def run_analytical_pipeline(db: Session, user_id: str):
    profile = analyze_user_spending(db, user_id)
    rec = generate_recommendation(db, user_id, profile)
    risk = calculate_personalized_risk(db, user_id, profile, rec)
    generate_insights(db, user_id, profile, rec.gap)
    return {"profile": profile, "recommendation": rec, "risk": risk}
