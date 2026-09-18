"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "menteeId": "...", "needs": { "budgetMax": 0, "timeframeWeeks": 0, "language": "..." } }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "mentors": [ { "mentorId": "...", "score": 0.0, "reason": "..." } ] }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
