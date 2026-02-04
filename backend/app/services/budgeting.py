from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Transaction


def generate_budget_plan(db: Session):
    """
    AI-driven recommended monthly budget plan
    based on historical monthly category spending
    """

    results = (
        db.query(
            func.upper(func.coalesce(Transaction.category, "OTHER")).label("category"),
            func.avg(Transaction.amount).label("avg_spent"),
            func.count(Transaction.id).label("txn_count"),
        )
        .group_by(func.upper(func.coalesce(Transaction.category, "OTHER")))
        .all()
    )

    budget_plan = []

    for row in results:
        category = row.category
        avg_spent = float(row.avg_spent or 0)

        # Smart recommendation rules
        if avg_spent > 5000:
            recommended = avg_spent * 0.85
        elif avg_spent > 2000:
            recommended = avg_spent * 0.90
        else:
            recommended = max(avg_spent * 0.95, 500)  # minimum realistic budget

        budget_plan.append({
            "category": category,
            "average_spent": round(avg_spent, 2),
            "recommended_budget": round(recommended, 2),
            "saving_target": round(avg_spent - recommended, 2),
            "transactions_analyzed": row.txn_count
        })

    return {
        "monthly_budget_plan": sorted(
            budget_plan, key=lambda x: x["average_spent"], reverse=True
        )
    }
