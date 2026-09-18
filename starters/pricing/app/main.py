"""
U-CS 6 — AI Pricing Optimization

  POST /price
    in : { "mentorId": "..." }
    out: { "min": 0, "max": 0, "comparables": [], "reason": "..." }

Do not change the shape without agreeing it with: U-CS 7 (analytics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 6 — pricing", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/price", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
