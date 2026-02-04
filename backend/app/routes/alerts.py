from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.services.alerts_service import generate_budget_alerts
from app.schemas.alerts import BudgetAlert

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/budget-breach", response_model=List[BudgetAlert])
def get_budget_alerts(
    month: str,
    db: Session = Depends(get_db)
):
    return generate_budget_alerts(db, month)
