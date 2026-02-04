from pydantic import BaseModel
from typing import Optional


class BudgetCreate(BaseModel):
    category: str
    month: str
    monthly_budget: float



class BudgetResponse(BaseModel):
    id: int
    category: str
    monthly_budget: float

    class Config:
        from_attributes = True
