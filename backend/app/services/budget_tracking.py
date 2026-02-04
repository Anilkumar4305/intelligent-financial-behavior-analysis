from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Transaction, Budget


def get_budget_vs_actual(db: Session, month: str):
    """
    Compare budget vs actual spending for a given month (YYYY-MM)
    """

    # -----------------------------------
    # 1️⃣ Actual spending per category
    # -----------------------------------
    actuals = (
        db.query(
            func.upper(func.coalesce(Transaction.category, "OTHER")).label("category"),
            func.sum(Transaction.amount).label("actual_spent"),
        )
        .filter(func.date_format(Transaction.date, "%Y-%m") == month)
        .group_by(func.upper(func.coalesce(Transaction.category, "OTHER")))
        .all()
    )

    # -----------------------------------
    # 2️⃣ Budgets
    # -----------------------------------
    budgets = (
        db.query(
            func.upper(Budget.category).label("category"),
            Budget.monthly_budget,
        )
        .filter(Budget.month == month)
        .all()
    )

    budget_map = {b.category: float(b.monthly_budget) for b in budgets}
    actual_map = {a.category: float(a.actual_spent) for a in actuals}

    # Include categories that exist in either budgets or spending
    all_categories = set(budget_map.keys()) | set(actual_map.keys())

    response = []

    for category in all_categories:
        budgeted = budget_map.get(category, 0.0)
        actual = actual_map.get(category, 0.0)

        diff = actual - budgeted
        percent_used = (actual / budgeted * 100) if budgeted > 0 else 0

        response.append({
            "category": category,
            "budgeted_amount": round(budgeted, 2),
            "actual_spent": round(actual, 2),
            "difference": round(diff, 2),  # keep sign
            "percent_used": round(percent_used, 1),
            "status": (
                "Exceeded" if diff > 0 else
                "Near Limit" if percent_used >= 90 else
                "Under Budget"
            )
        })

    return sorted(response, key=lambda x: x["percent_used"], reverse=True)
