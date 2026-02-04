"""
Utility script to create database tables.

Run:
    python -m backend.create_tables
"""

import sys
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine
from app.db.models import Base  # import Base directly


def create_tables():
    try:
        print("📦 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")

    except SQLAlchemyError as e:
        print("❌ Database table creation failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_tables()
