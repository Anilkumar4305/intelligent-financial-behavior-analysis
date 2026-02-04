from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db

from app.services.analytics_summary_service import build_analytics_summary
from app.services.health_score import calculate_financial_health_score
from app.services.recommendations import generate_recommendations
from app.services.budgeting import generate_budget_plan
from app.services.risk_alerts import generate_financial_risk_alerts
from app.services.aggregation import (
    get_monthly_spend,
    get_category_trends,
    get_budget_vs_actual
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# -------------------------------------------------
# BASIC ANALYTICS
# -------------------------------------------------

@router.get("/monthly-spend")
def monthly_spend(db: Session = Depends(get_db)):
    return get_monthly_spend(db)


@router.get("/category-trends")
def category_trends(db: Session = Depends(get_db)):
    # Return plain array for charts
    return get_category_trends(db)


@router.get("/financial-health")
def financial_health(db: Session = Depends(get_db)):
    return calculate_financial_health_score(db)


@router.get("/recommendations")
def recommendations(db: Session = Depends(get_db)):
    return generate_recommendations(db)


@router.get("/budget-plan")
def budget_plan(db: Session = Depends(get_db)):
    return generate_budget_plan(db)


@router.get("/risk-alerts")
def risk_alerts(db: Session = Depends(get_db)):
    return generate_financial_risk_alerts(db)


# -------------------------------------------------
# 🔥 FIXED BUDGET VS ACTUAL (MATCH FRONTEND)
# -------------------------------------------------
@router.get("/budget-vs-actual")
def budget_vs_actual(
    month: str = Query(..., description="YYYY-MM"),
    db: Session = Depends(get_db)
):
    raw = get_budget_vs_actual(db, month)

    return [
        {
            "category": r["category"],
            "budget": r["budgeted_amount"],
            "actual": r["actual_spent"],
        }
        for r in raw
    ]


# -------------------------------------------------
# 🔥 FIXED SUMMARY ENDPOINT (FRONTEND FORMAT)
# -------------------------------------------------
@router.get("/summary")
def analytics_summary(
    month: str = Query(...),
    db: Session = Depends(get_db)
):
    data = build_analytics_summary(db, month)

    return {
        "health_score": data.health_score,
        "monthly_spend": data.monthly_spend,
        "top_category": data.top_category,
        "category_breakdown": data.category_breakdown,
        "budget_vs_actual": data.budget_vs_actual,
        "risk_alerts": data.risk_alerts,
        "recommendations": data.recommendations,
        "explanations": data.explanations,
    }
