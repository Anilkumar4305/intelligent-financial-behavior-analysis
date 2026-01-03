from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.categorization import categorize_transaction

from typing import List
import csv
import io
import datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Temporary in-memory storage (NO database yet)
fake_db = []
transaction_id_counter = 1


# -----------------------------
# CREATE SINGLE TRANSACTION
# -----------------------------
@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    global transaction_id_counter

    # Phase 3.1 – AI Categorization
    category, confidence, method = categorize_transaction(
        transaction.description
    )

    new_transaction = {
        "id": transaction_id_counter,
        "date": transaction.date,
        "amount": transaction.amount,
        "description": transaction.description,
        "platform": transaction.platform,
        "source": "manual",
        "category": category,
        "confidence": confidence,
        "classification_method": method
    }

    fake_db.append(new_transaction)
    transaction_id_counter += 1

    return new_transaction


# -----------------------------
# GET ALL TRANSACTIONS
# -----------------------------
@router.get("/", response_model=List[TransactionResponse])
def get_transactions():
    return fake_db


# -----------------------------
# BULK MANUAL INPUT
# -----------------------------
@router.post("/bulk", response_model=List[TransactionResponse])
def create_bulk_transactions(transactions: List[TransactionCreate]):
    global transaction_id_counter

    created_transactions = []

    for transaction in transactions:
        category, confidence, method = categorize_transaction(
            transaction.description
        )

        new_transaction = {
            "id": transaction_id_counter,
            "date": transaction.date,
            "amount": transaction.amount,
            "description": transaction.description,
            "platform": transaction.platform,
            "source": "manual",
            "category": category,
            "confidence": confidence,
            "classification_method": method
        }

        fake_db.append(new_transaction)
        created_transactions.append(new_transaction)
        transaction_id_counter += 1

    return created_transactions


# -----------------------------
# CSV UPLOAD
# -----------------------------
@router.post("/upload-csv", response_model=List[TransactionResponse])
def upload_transactions_csv(file: UploadFile = File(...)):
    global transaction_id_counter

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    content = file.file.read().decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(content))

    required_columns = {"date", "amount", "description", "platform"}
    if not required_columns.issubset(csv_reader.fieldnames):
        raise HTTPException(
            status_code=400,
            detail="CSV must contain date, amount, description, platform columns"
        )

    created_transactions = []

    for row in csv_reader:
        try:
            category, confidence, method = categorize_transaction(
                row["description"]
            )

            new_transaction = {
                "id": transaction_id_counter,
                "date": datetime.date.fromisoformat(row["date"]),
                "amount": float(row["amount"]),
                "description": row["description"],
                "platform": row["platform"],
                "source": "csv",
                "category": category,
                "confidence": confidence,
                "classification_method": method
            }

            fake_db.append(new_transaction)
            created_transactions.append(new_transaction)
            transaction_id_counter += 1

        except Exception:
            raise HTTPException(status_code=400, detail="Invalid data in CSV file")

    return created_transactions
