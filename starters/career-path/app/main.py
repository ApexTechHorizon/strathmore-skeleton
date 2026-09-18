"""
U-CS 1 — AI Career Path Recommendation

  POST /paths
    in : { "profile": {} }
    out: { "paths": [ { "roleId": "...", "reachability": 0.0, "missingSkills": [], "reason": "..." } ] }

Do not change the shape without agreeing it with: U-CS 8 (micro-learning)
"""
from fastapi import FastAPI

from app.schemas import Request, Response
from app.service import handle

app = FastAPI(title="U-CS 1 — career-path", version="0.1.0")


@app.get("/health")
def health():
    """Hosting platforms call this to check the service is alive."""
    return {"status": "ok"}


@app.post("/paths", response_model=Response)
def endpoint(body: Request) -> Response:
    return handle(body)
