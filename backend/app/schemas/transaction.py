from pydantic import BaseModel, Field
import datetime
from typing import Optional


class TransactionBase(BaseModel):
    date: datetime.date = Field(..., example="2025-08-12")
    amount: float = Field(..., gt=0, example=450.0)
    description: str = Field(..., example="Swiggy food order")
    platform: str = Field(..., example="PhonePe")


class TransactionCreate(TransactionBase):
    """
    Schema used when creating a new transaction
    """
    pass


class TransactionResponse(TransactionBase):
    """
    Schema returned to the client
    """
    id: int
    source: Optional[str] = None

    # Phase 3.1 – AI classification output
    category: Optional[str] = None
    confidence: Optional[float] = None
    classification_method: Optional[str] = None

    class Config:
        from_attributes = True
