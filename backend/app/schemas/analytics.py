from pydantic import BaseModel
from typing import List, Dict, Optional


# -------------------------
# BASIC ANALYTICS MODELS
# -------------------------

class MonthlySpend(BaseModel):
    month: str
    total_spent: float


class CategoryTrendItem(BaseModel):
    month: str
    amount: float


# Category trends response (USED BY ROUTES)
CategoryTrendsResponse = Dict[str, List[CategoryTrendItem]]


# -------------------------
# BUDGET VS ACTUAL (FRONTEND SAFE)
# -------------------------

class BudgetVsActual(BaseModel):
    budget: float
    actual: float


# -------------------------
# UNIFIED ANALYTICS SUMMARY
# -------------------------

class AnalyticsSummaryResponse(BaseModel):
    """
    Unified analytics response used by Dashboard
    """

    health_score: int
    monthly_spend: float
    top_category: Optional[str]

    # REQUIRED BY FRONTEND CHARTS
    category_breakdown: Dict[str, float]
    budget_vs_actual: BudgetVsActual

    # TEXT SECTIONS
    risk_alerts: List[str]
    recommendations: List[str]
    explanations: List[str]