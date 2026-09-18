"""
U-CS 3 — Skills Gap & Trust Scoring

  POST /gap
    in : { "profile": {}, "targetRole": "..." }
    out: { "have": [], "missing": [ { "skill": "...", "confidence": 0.0 } ], "readiness": 0.0 }

Do not change the shape without agreeing it with: U-CS 1 (career-path) and U-CS 8 (micro-learning)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 3 — skills-gap", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/gap", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
