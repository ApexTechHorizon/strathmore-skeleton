"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "dependantId": "..." }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "oneYear": 0, "fiveYear": 0, "tenYear": 0, "peakYear": 2036, "breakdown": {}, "assumptions": [] }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
