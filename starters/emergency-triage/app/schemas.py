"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "type": "...", "context": {}, "geo": { "lat": 0.0, "lng": 0.0 } }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "priority": "HIGH", "routeTo": "...", "escalateAfterMins": 5, "fallbackChannel": "SMS" }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
