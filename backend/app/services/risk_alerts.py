from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.db.models import Transaction


def generate_financial_risk_alerts(db: Session, month: str):

    alerts = []

    try:
        current_month = datetime.strptime(month, "%Y-%m")
    except ValueError:
        return {"risk_alerts": [], "total_alerts": 0}

    prev_month = (current_month - relativedelta(months=1)).strftime("%Y-%m")

    # Monthly totals
    def get_total(m):
        return (
            db.query(func.sum(Transaction.amount))
            .filter(func.date_format(Transaction.date, "%Y-%m") == m)
            .scalar()
        ) or 0

    current_total = get_total(month)
    previous_total = get_total(prev_month)

    # Category distribution
    category_data = (
        db.query(
            func.upper(func.coalesce(Transaction.category, "OTHER")).label("category"),
            func.sum(Transaction.amount).label("total")
        )
        .filter(func.date_format(Transaction.date, "%Y-%m") == month)
        .group_by("category")
        .all()
    )

    for row in category_data:
        percent = (float(row.total) / current_total * 100) if current_total else 0
        if percent > 45:
            alerts.append({
                "risk_type": "Category Imbalance",
                "severity": "High",
                "message": f"{row.category} spending is {percent:.1f}% of total."
            })

    # Spending spike
    if previous_total > 0:
        change = ((current_total - previous_total) / previous_total) * 100
        if change > 30:
            alerts.append({
                "risk_type": "Spending Spike",
                "severity": "Medium",
                "message": f"Spending increased by {change:.1f}% from last month."
            })

    # Transaction frequency
    txn_count = (
        db.query(func.count(Transaction.id))
        .filter(func.date_format(Transaction.date, "%Y-%m") == month)
        .scalar()
    ) or 0

    if txn_count > 180:
        alerts.append({
            "risk_type": "High Transaction Volume",
            "severity": "Low",
            "message": "Large number of transactions may indicate impulse spending."
        })

    return {"risk_alerts": alerts, "total_alerts": len(alerts)}
