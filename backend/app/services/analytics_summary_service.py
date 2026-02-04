from sqlalchemy.orm import Session
from sqlalchemy import func

from app.services.health_score import calculate_financial_health_score
from app.services.recommendations import generate_recommendations
from app.services.risk_alerts import generate_financial_risk_alerts
from app.services.analytics_summary_explainer import generate_summary_explanation

from app.services.aggregation import get_budget_vs_actual
from app.db.models import Transaction
from app.schemas.analytics import AnalyticsSummaryResponse


def build_analytics_summary(db: Session, month: str) -> AnalyticsSummaryResponse:
    """
    Builds unified analytics response for dashboard
    """

    # ---------------------------------------------------
    # 1️⃣ Financial Health Score
    # ---------------------------------------------------
    health_data = calculate_financial_health_score(db)
    health_score = health_data.get("score", 0)

    # ---------------------------------------------------
    # 2️⃣ Monthly Spend (selected month)
    # ---------------------------------------------------
    monthly_spend_result = (
        db.query(func.sum(Transaction.amount))
        .filter(func.date_format(Transaction.date, "%Y-%m") == month)
        .scalar()
    )
    monthly_spend = float(monthly_spend_result or 0)

    # ---------------------------------------------------
    # 3️⃣ Category Breakdown (selected month)
    # ---------------------------------------------------
    category_results = (
        db.query(
            func.coalesce(func.upper(Transaction.category), "OTHER"),
            func.sum(Transaction.amount)
        )
        .filter(func.date_format(Transaction.date, "%Y-%m") == month)
        .group_by(func.coalesce(func.upper(Transaction.category), "OTHER"))
        .all()
    )

    category_breakdown = {
        category: float(amount or 0)
        for category, amount in category_results
    }

    # ---------------------------------------------------
    # 4️⃣ Top Category
    # ---------------------------------------------------
    top_category = (
        max(category_breakdown, key=category_breakdown.get)
        if category_breakdown else None
    )

    # ---------------------------------------------------
    # 5️⃣ Budget vs Actual (TOTALS)
    # ---------------------------------------------------
    budget_vs_actual = get_budget_vs_actual(db, month)

    # ---------------------------------------------------
    # 6️⃣ Risk Alerts
    # ---------------------------------------------------
    risk_data = generate_financial_risk_alerts(db, month)
    risk_alerts = [
        alert["message"]
        for alert in risk_data.get("risk_alerts", [])
    ]

    # ---------------------------------------------------
    # 7️⃣ Recommendations
    # ---------------------------------------------------
    recommendations_data = generate_recommendations(db)
    recommendations = [
        rec["message"]
        for rec in recommendations_data.get("recommendations", [])
    ]

    # ---------------------------------------------------
    # 8️⃣ AI Explanations
    # ---------------------------------------------------
    explanations = generate_summary_explanation(
        health_score=health_score,
        monthly_spend=monthly_spend,
        top_category=top_category,
        risk_alerts=risk_alerts
    )

    # ---------------------------------------------------
    # 9️⃣ Final Schema Response
    # ---------------------------------------------------
    return AnalyticsSummaryResponse(
        health_score=health_score,
        monthly_spend=monthly_spend,
        top_category=top_category,
        category_breakdown=category_breakdown,
        budget_vs_actual=budget_vs_actual,
        risk_alerts=risk_alerts,
        recommendations=recommendations,
        explanations=explanations,
    )
