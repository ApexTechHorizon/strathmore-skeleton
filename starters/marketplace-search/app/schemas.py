"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "q": "plumber", "categoryId": "...", "lat": 0.0, "lng": 0.0 }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "results": [ { "serviceId": "...", "score": 0.0, "why": "..." } ] }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
