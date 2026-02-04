from sqlalchemy import Column, Integer, String, Float, Date
from app.db.database import Base


# -----------------------------
# TRANSACTIONS TABLE
# -----------------------------
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    platform = Column(String(50), nullable=False)
    source = Column(String(20), default="manual")

    # AI Classification Fields (Phase 3)
    category = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=True)
    classification_method = Column(String(30), nullable=True)


# -----------------------------
# BUDGETS TABLE (Phase 5)
# -----------------------------
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)

    # Category name (FOOD, SHOPPING, etc.)
    category = Column(String(50), nullable=False)

    # Month in YYYY-MM format (e.g., 2026-01)
    month = Column(String(7), nullable=False)

    # Planned budget amount
    monthly_budget = Column(Float, nullable=False)  # 🔥 rename from 'amount'

