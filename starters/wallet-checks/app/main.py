"""
U-CS 42 — Wallet & Escrow

  POST /ledger/verify
    in : { "from": "2026-01-01", "to": "2026-01-31" }
    out: { "balanced": true, "discrepancies": [] }

Do not change the shape without agreeing it with: U-CS 46 (ops-metrics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 42 — wallet-checks", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/ledger/verify", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
