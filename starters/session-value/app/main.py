"""
U-CS 5 — Session Effectiveness Predictor

  POST /predict
    in : { "menteeId": "...", "mentorId": "...", "leadTimeHours": 0, "hasAgenda": false, "isFirstSession": true }
    out: { "probability": 0.0, "factors": [], "suggestedIntervention": "..." }

Do not change the shape without agreeing it with: U-CS 7 (analytics)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 5 — session-value", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/predict", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
