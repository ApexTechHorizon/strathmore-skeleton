"""
U-CS 43 — Dependants Budget Management

  POST /projection
    in : { "dependantId": "..." }
    out: { "oneYear": 0, "fiveYear": 0, "tenYear": 0, "peakYear": 2036, "breakdown": {}, "assumptions": [] }

Do not change the shape without agreeing it with: U-CS 46 (ops-metrics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 43 — dependant-costs", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/projection", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
