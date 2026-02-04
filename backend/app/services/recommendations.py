from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Transaction
import statistics


def generate_recommendations(db: Session):

    recommendations = []

    # -------------------------
    # Monthly spending trend
    # -------------------------
    monthly_data = (
        db.query(
            func.date_format(Transaction.date, "%Y-%m").label("month"),
            func.sum(Transaction.amount).label("total")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    totals = [float(row.total or 0) for row in monthly_data]

    if len(totals) >= 2 and totals[-2] > 0:
        growth = (totals[-1] - totals[-2]) / totals[-2]
        if growth > 0.30:
            recommendations.append({
                "type": "warning",
                "message": "Your spending jumped significantly last month.",
                "suggestion": "Audit recent transactions and cut optional expenses."
            })

    # -------------------------
    # Category concentration
    # -------------------------
    category_data = (
        db.query(
            func.upper(func.coalesce(Transaction.category, "OTHER")).label("category"),
            func.sum(Transaction.amount).label("total")
        )
        .group_by(func.upper(func.coalesce(Transaction.category, "OTHER")))
        .all()
    )

    overall = sum(float(row.total or 0) for row in category_data)

    for row in category_data:
        share = float(row.total or 0) / overall if overall else 0

        if share > 0.40:
            recommendations.append({
                "type": "advice",
                "message": f"'{row.category}' is consuming a large portion of your budget.",
                "suggestion": "Try reducing this category by 10–15%."
            })

    # -------------------------
    # Stability analysis
    # -------------------------
    if len(totals) >= 3:
        if statistics.stdev(totals) > 2500:
            recommendations.append({
                "type": "insight",
                "message": "Your spending fluctuates a lot month to month.",
                "suggestion": "Set fixed category budgets to stabilize finances."
            })

    if not recommendations:
        recommendations.append({
            "type": "positive",
            "message": "Your financial behavior looks balanced.",
            "suggestion": "Keep maintaining this consistency."
        })

    return {"recommendations": recommendations}
