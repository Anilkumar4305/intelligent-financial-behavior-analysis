from fastapi import APIRouter, HTTPException
from app.schemas.sms import SMSRequest
import re
from datetime import datetime

router = APIRouter(
    prefix="/sms",
    tags=["SMS Ingestion"]
)

@router.post("/ingest")
def ingest_sms(data: SMSRequest):
    if not data.message:
        raise HTTPException(status_code=400, detail="SMS message is empty")

    text = data.message.lower()

    # -----------------------------
    # Extract amount (Rs / INR)
    # -----------------------------
    amount_match = re.search(r"(rs\.?|inr)\s?(\d+(?:\.\d+)?)", text)
    if not amount_match:
        raise HTTPException(status_code=400, detail="Amount not found in SMS")

    amount = float(amount_match.group(2))
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid transaction amount")

    # -----------------------------
    # Extract date (DD-MM-YYYY or DD/MM/YYYY)
    # -----------------------------
    date_match = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", text)
    if date_match:
        day, month, year = date_match.groups()
        date = datetime(int(year), int(month), int(day)).date()
    else:
        date = datetime.today().date()

    # -----------------------------
    # Identify platform
    # -----------------------------
    platform = "UNKNOWN"
    if "gpay" in text or "google pay" in text:
        platform = "GPAY"
    elif "phonepe" in text:
        platform = "PHONEPE"
    elif "paytm" in text:
        platform = "PAYTM"

    description = "SMS Transaction"

    return {
        "status": "parsed",
        "data": {
            "amount": amount,
            "date": date,
            "platform": platform,
            "description": description,
            "source": "SMS"
        }
    }
