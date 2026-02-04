from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import csv
import io
import datetime

from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.categorization import categorize_transaction
from app.db.database import get_db
from app.db.models import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# -------------------------------------------------
# CREATE SINGLE TRANSACTION
# -------------------------------------------------
@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        category, confidence, method = categorize_transaction(transaction.description)

        db_transaction = Transaction(
            date=transaction.date,
            amount=transaction.amount,
            description=transaction.description,
            platform=transaction.platform,
            source="manual",
            category=category,
            confidence=confidence,
            classification_method=method,
        )

        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction creation failed: {str(e)}")


# -------------------------------------------------
# GET TRANSACTIONS (PAGINATED + FILTERS)
# -------------------------------------------------
@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if category:
        query = query.filter(Transaction.category == category.upper())

    if search:
        query = query.filter(
            or_(
                Transaction.description.ilike(f"%{search}%"),
                Transaction.platform.ilike(f"%{search}%")
            )
        )

    return (
        query.order_by(Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# -------------------------------------------------
# BULK CREATE TRANSACTIONS
# -------------------------------------------------
@router.post("/bulk", response_model=List[TransactionResponse])
def create_bulk_transactions(transactions: List[TransactionCreate], db: Session = Depends(get_db)):
    db_transactions = []

    try:
        for transaction in transactions:
            category, confidence, method = categorize_transaction(transaction.description)

            db_transactions.append(
                Transaction(
                    date=transaction.date,
                    amount=transaction.amount,
                    description=transaction.description,
                    platform=transaction.platform,
                    source="manual",
                    category=category,
                    confidence=confidence,
                    classification_method=method,
                )
            )

        db.bulk_save_objects(db_transactions)
        db.commit()

        for tx in db_transactions:
            db.refresh(tx)

        return db_transactions

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Bulk insert failed: {str(e)}")


# -------------------------------------------------
# CSV UPLOAD
# -------------------------------------------------
@router.post("/upload-csv", response_model=List[TransactionResponse])
def upload_transactions_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        content = file.file.read().decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    required_columns = {"date", "amount", "description", "platform"}
    if not required_columns.issubset(set(csv_reader.fieldnames or [])):
        raise HTTPException(status_code=400, detail="CSV missing required columns")

    created = []
    errors = []

    for i, row in enumerate(csv_reader, start=1):
        try:
            date = datetime.date.fromisoformat(row["date"])
            amount = float(row["amount"])
            description = row["description"]
            platform = row["platform"]

            category, confidence, method = categorize_transaction(description)

            tx = Transaction(
                date=date,
                amount=amount,
                description=description,
                platform=platform,
                source="csv",
                category=category,
                confidence=confidence,
                classification_method=method,
            )

            db.add(tx)
            created.append(tx)

        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    if not created:
        raise HTTPException(status_code=400, detail=f"No valid rows found. Errors: {errors}")

    db.commit()
    for tx in created:
        db.refresh(tx)

    return created
