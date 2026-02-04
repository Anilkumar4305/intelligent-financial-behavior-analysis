from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.services.budget_service import create_budget, get_all_budgets

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetResponse)
def add_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    return create_budget(
        db=db,
        category=budget.category.strip().upper(),
        month=budget.month,
        monthly_budget=budget.monthly_budget
    )


@router.get("/", response_model=List[BudgetResponse])
def list_budgets(db: Session = Depends(get_db)):
    return get_all_budgets(db)
