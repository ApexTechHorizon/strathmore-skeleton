"""
U-CS 8 — Micro-Learning Recommendation

  POST /next
    in : { "userId": "...", "gap": [] }
    out: { "lessons": [ { "lessonId": "...", "why": "...", "prereqsMet": true } ] }

Do not change the shape without agreeing it with: U-CS 4 (chatbot)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 8 — micro-learning", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/next", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
