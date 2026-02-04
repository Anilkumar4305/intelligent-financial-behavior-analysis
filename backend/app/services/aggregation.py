from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Transaction, Budget


# ---------------------------------------------------------
# MONTHLY SPEND
# ---------------------------------------------------------
def get_monthly_spend(db: Session):
    results = (
        db.query(
            func.date_format(Transaction.date, "%Y-%m").label("month"),
            func.sum(Transaction.amount).label("total_spent"),
        )
        .group_by(func.date_format(Transaction.date, "%Y-%m"))
        .order_by(func.date_format(Transaction.date, "%Y-%m"))
        .all()
    )

    return [
        {"month": row.month, "total_spent": float(row.total_spent or 0)}
        for row in results
    ]


# ---------------------------------------------------------
# CATEGORY TRENDS
# ---------------------------------------------------------
def get_category_trends(db: Session):
    results = (
        db.query(
            func.date_format(Transaction.date, "%Y-%m").label("month"),
            func.coalesce(Transaction.category, "OTHER").label("category"),
            func.sum(Transaction.amount).label("total_spent"),
        )
        .group_by(
            func.date_format(Transaction.date, "%Y-%m"),
            func.coalesce(Transaction.category, "OTHER"),
        )
        .order_by(func.date_format(Transaction.date, "%Y-%m"))
        .all()
    )

    trends = {}

    for row in results:
        trends.setdefault(row.category, []).append(
            {"month": row.month, "amount": float(row.total_spent or 0)}
        )

    return trends


# ---------------------------------------------------------
# BUDGET VS ACTUAL (MATCHES SCHEMA)
# ---------------------------------------------------------
def get_budget_vs_actual(db: Session, month: str):
    # ---- Budgets ----
    budgets = (
        db.query(
            func.upper(Budget.category).label("category"),
            func.sum(Budget.monthly_budget).label("budget"),
        )
        .filter(Budget.month == month)
        .group_by(func.upper(Budget.category))
        .all()
    )

    budget_map = {b.category: float(b.budget or 0) for b in budgets}

    # ---- Actual spending ----
    actuals = (
        db.query(
            func.coalesce(func.upper(Transaction.category), "OTHER").label("category"),
            func.sum(Transaction.amount).label("actual"),
        )
        .filter(func.date_format(Transaction.date, "%Y-%m") == month)
        .group_by(func.coalesce(func.upper(Transaction.category), "OTHER"))
        .all()
    )

    actual_map = {a.category: float(a.actual or 0) for a in actuals}

    # ---- Combine ----
    total_budget = sum(budget_map.values())
    total_actual = sum(actual_map.values())

    return {
        "budget": total_budget,
        "actual": total_actual,
    }
