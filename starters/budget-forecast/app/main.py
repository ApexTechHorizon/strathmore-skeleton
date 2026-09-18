"""
U-CS 37 — AI Lifestyle Budgeting & Cost Modeling

  POST /forecast
    in : { "userId": "...", "month": 6, "year": 2026 }
    out: { "estimatedTotal": 0, "breakdown": {}, "confidence": 0.0, "riskFlag": null }

Do not change the shape without agreeing it with: U-CS 38 (spend-advisor), U-CS 43 (dependant-costs), U-CS 46 (ops-metrics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 37 — budget-forecast", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/forecast", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
