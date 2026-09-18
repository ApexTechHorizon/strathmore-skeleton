"""
U-CS 4 — AI Career Coaching Chatbot

  POST /ask
    in : { "question": "...", "userId": "..." }
    out: { "answer": "...", "citations": [], "handover": false, "handoverReason": null }

Do not change the shape without agreeing it with: Nobody directly — but you are what makes mentor time go further.
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 4 — chatbot", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/ask", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
