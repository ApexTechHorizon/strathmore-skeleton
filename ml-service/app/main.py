"""
Your service. Replace the placeholder endpoint with the one from your card
in the Team Integration Map. Keep the shape exactly as agreed — other teams
call this.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="<YOUR USE CASE> service")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


class PredictIn(BaseModel):
    # Replace with the real input from your contract
    userId: str


class PredictOut(BaseModel):
    # Replace with the real output from your contract
    score: float
    reason: str


@app.post("/predict", response_model=PredictOut)
def predict(body: PredictIn) -> PredictOut:
    # STEP 1 — the baseline. The dumbest thing that works.
    #          Measure it. Write the number down. Only then improve it.
    return PredictOut(score=0.5, reason="baseline: constant prediction")
