from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.transactions import router as transactions_router
from app.routes import sms


app = FastAPI(
    title="Intelligent Financial Behavior Analysis API",
    description="Backend API for expense ingestion and analysis",
    version="0.1.0"
)

app.include_router(sms.router)
app.include_router(health_router)
app.include_router(transactions_router)
