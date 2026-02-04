from sqlalchemy.orm import Session
from app.db.models import Budget


def create_budget(db: Session, category: str, month: str, monthly_budget: float):
    budget = Budget(
        category=category.upper(),
        month=month,
        monthly_budget=monthly_budget,
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_all_budgets(db: Session):
    return db.query(Budget).order_by(Budget.month.desc()).all()
