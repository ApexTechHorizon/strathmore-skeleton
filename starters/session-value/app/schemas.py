"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "menteeId": "...", "mentorId": "...", "leadTimeHours": 0, "hasAgenda": false, "isFirstSession": true }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "probability": 0.0, "factors": [], "suggestedIntervention": "..." }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
