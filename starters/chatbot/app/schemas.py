"""The contract, as validated types. Other teams depend on these shapes."""
from typing import Any
from pydantic import BaseModel


class Request(BaseModel):
    """in : { "question": "...", "userId": "..." }"""
    # TODO — replace with the real fields
    model_config = {"extra": "allow"}


class Response(BaseModel):
    """out: { "answer": "...", "citations": [], "handover": false, "handoverReason": null }"""
    # TODO — replace with the real fields
    isSynthetic: bool = True
    method: str = "baseline"
    model_config = {"extra": "allow"}
