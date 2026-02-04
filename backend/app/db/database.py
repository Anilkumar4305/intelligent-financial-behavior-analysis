from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection URL
DATABASE_URL = (
    "mysql+pymysql://root:9666@127.0.0.1:3306/db_financial_behaviour"
)

# Create engine (NO table creation here)
engine = create_engine(
    DATABASE_URL,
    echo=True,          # logs SQL (good for learning)
    pool_pre_ping=True  # avoids stale connections
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency (used in routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
