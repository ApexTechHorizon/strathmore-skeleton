"""
U-CS 7 — Institution Impact Analytics

  POST /cohort
    in : { "cohortId": "..." }
    out: { "engagement": {}, "progression": {}, "outcomes": {}, "caveats": [] }

Do not change the shape without agreeing it with: Nobody. You are the end of the line.
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 7 — analytics", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/cohort", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
