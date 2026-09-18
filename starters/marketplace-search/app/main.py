"""
U-CS 39 — Lifestyle Marketplace

  POST /search
    in : { "q": "plumber", "categoryId": "...", "lat": 0.0, "lng": 0.0 }
    out: { "results": [ { "serviceId": "...", "score": 0.0, "why": "..." } ] }

Do not change the shape without agreeing it with: U-CS 40 (provider-match) uses your ranking signals
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 39 — marketplace-search", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/search", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
