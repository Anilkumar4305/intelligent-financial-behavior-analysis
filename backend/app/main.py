from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transactions   # or correct import path


# DB Base (for future auto table creation if needed)
from app.db.database import Base, engine

# -----------------------------
# Import Routers
# -----------------------------
from app.routes.health import router as health_router
from app.routes.transactions import router as transactions_router
from app.routes.analytics import router as analytics_router
from app.routes.budget import router as budget_router
from app.routes.sms import router as sms_router


# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI(
    title="Intelligent Financial Behavior Analysis API",
    description="AI-powered backend for expense ingestion, analytics, and insights",
    version="1.0.0",
)


# -----------------------------
# CORS CONFIGURATION
# -----------------------------
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# API ROUTER REGISTRATION
# -----------------------------
API_PREFIX = "/api"

app.include_router(health_router, prefix=API_PREFIX)
app.include_router(transactions_router, prefix=API_PREFIX)
app.include_router(analytics_router, prefix=API_PREFIX)
app.include_router(budget_router, prefix=API_PREFIX)
app.include_router(sms_router, prefix=API_PREFIX)
app.include_router(transactions.router)

# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.get("/")
def root():
    return {
        "name": "Intelligent Financial Behavior Analysis API",
        "status": "running",
        "version": "1.0.0"
    }


# -----------------------------
# STARTUP EVENT
# -----------------------------
@app.on_event("startup")
def startup_event():
    # Optional: auto-create tables if they don't exist
    # Safe for dev, comment in production if using migrations
    Base.metadata.create_all(bind=engine)

    print("🚀 Backend API started successfully")
