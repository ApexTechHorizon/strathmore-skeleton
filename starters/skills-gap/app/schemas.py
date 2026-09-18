"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "profile": {}, "targetRole": "..." }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "have": [], "missing": [ { "skill": "...", "confidence": 0.0 } ], "readiness": 0.0 }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
