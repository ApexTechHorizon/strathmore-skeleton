"""
U-CS 41 — Smart Scheduling

  POST /noshow/predict
    in : { "bookingId": "..." }
    out: { "probability": 0.0, "factors": [] }

Do not change the shape without agreeing it with: U-CS 46 (ops-metrics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 41 — scheduling", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/noshow/predict", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
