"""
U-CS 2 — Intelligent Mentor Matching

  POST /match
    in : { "menteeId": "...", "needs": { "budgetMax": 0, "timeframeWeeks": 0, "language": "..." } }
    out: { "mentors": [ { "mentorId": "...", "score": 0.0, "reason": "..." } ] }

Do not change the shape without agreeing it with: U-CS 5 (session-value), U-CS 6 (pricing), U-CS 7 (analytics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 2 — matching", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/match", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
