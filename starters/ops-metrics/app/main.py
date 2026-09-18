"""
U-CS 46 — Lifestyle Analytics Dashboard

  POST /metrics
    in : { "from": "2026-01-01", "to": "2026-01-31" }
    out: { "metrics": [ { "name": "...", "value": 0, "definition": "...", "decisionItSupports": "..." } ] }

Do not change the shape without agreeing it with: Nobody. You are the end of the line.
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 46 — ops-metrics", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/metrics", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
