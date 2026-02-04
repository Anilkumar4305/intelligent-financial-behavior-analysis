from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Transaction
import statistics


def calculate_financial_health_score(db: Session):
    """
    AI-style financial health scoring
    Score Range: 0 – 100
    """

    score = 100
    reasons = []

    # --------------------------------------------------
    # 1️⃣ Monthly Spending Stability
    # --------------------------------------------------
    monthly_totals = (
        db.query(
            func.date_format(Transaction.date, "%Y-%m").label("month"),
            func.sum(Transaction.amount).label("total"),
        )
        .group_by(func.date_format(Transaction.date, "%Y-%m"))
        .order_by(func.date_format(Transaction.date, "%Y-%m"))
        .all()
    )

    totals = [float(row.total or 0) for row in monthly_totals]

    if len(totals) >= 2:
        std_dev = statistics.stdev(totals)

        if std_dev > 3000:
            score -= 20
            reasons.append("High month-to-month spending variation detected")
        else:
            reasons.append("Spending pattern is stable across months")

    # --------------------------------------------------
    # 2️⃣ Category Concentration Risk
    # --------------------------------------------------
    category_totals = (
        db.query(
            func.coalesce(Transaction.category, "OTHER"),
            func.sum(Transaction.amount).label("total"),
        )
        .group_by(func.coalesce(Transaction.category, "OTHER"))
        .all()
    )

    overall_spent = sum(float(row.total or 0) for row in category_totals)

    if overall_spent > 0:
        for row in category_totals:
            share = float(row.total or 0) / overall_spent

            if share > 0.5:
                score -= 15
                reasons.append(
                    f"Overspending risk: '{row[0]}' dominates your expenses"
                )

    # --------------------------------------------------
    # 3️⃣ Overspending Spike Detection
    # --------------------------------------------------
    if len(totals) >= 2 and totals[-1] > 1.4 * totals[-2]:
        score -= 20
        reasons.append("Sudden spending spike detected in recent month")

    # --------------------------------------------------
    # Clamp score
    # --------------------------------------------------
    score = max(0, min(score, 100))

    return {
        "score": score,  # ✅ MUST match summary service
        "reasons": reasons,
    }
