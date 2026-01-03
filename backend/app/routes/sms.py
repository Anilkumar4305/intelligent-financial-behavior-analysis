from fastapi import APIRouter, HTTPException
from app.schemas.sms import SMSRequest
import re
from datetime import datetime

router = APIRouter(prefix="/api/sms", tags=["SMS Ingestion"])

@router.post("/ingest")
def ingest_sms(data: SMSRequest):
    text = data.message.lower()

    # Extract amount
    amount_match = re.search(r"(rs\.?|inr)\s?(\d+)", text)
    if not amount_match:
        raise HTTPException(status_code=400, detail="Amount not found in SMS")

    amount = float(amount_match.group(2))

    # Extract date (simple DD-MM-YYYY or DD/MM/YYYY)
    date_match = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", text)
    date = datetime.today().date()

    if date_match:
        day, month, year = date_match.groups()
        date = datetime(int(year), int(month), int(day)).date()

    # Identify platform (basic keywords)
    platform = "Unknown"
    if "gpay" in text:
        platform = "GPay"
    elif "phonepe" in text:
        platform = "PhonePe"
    elif "paytm" in text:
        platform = "Paytm"

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