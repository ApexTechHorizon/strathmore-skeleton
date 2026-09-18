"""
U-CS 38 — AI Spending Optimization

  POST /recommendations
    in : { "userId": "...", "month": 6, "year": 2026 }
    out: { "items": [ { "type": "...", "reason": "...", "savingKes": 0, "targetId": "..." } ] }

Do not change the shape without agreeing it with: U-CS 46 (ops-metrics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 38 — spend-advisor", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/recommendations", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
