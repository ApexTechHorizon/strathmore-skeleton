"""
U-CS 40 — AI Service Matching

  POST /match
    in : { "userId": "...", "categoryId": "...", "lat": 0.0, "lng": 0.0 }
    out: { "providers": [ { "providerId": "...", "score": 0.0, "reason": "..." } ] }

Do not change the shape without agreeing it with: U-CS 46 (ops-metrics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 40 — provider-match", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/match", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
