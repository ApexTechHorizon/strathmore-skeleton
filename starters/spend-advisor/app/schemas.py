"""U-CS38 contracts. Money stays decimal through JSON serialization."""
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, WithJsonSchema, field_validator

Identifier = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=128)]
Month = Annotated[int, Field(strict=True, ge=1, le=12)]
Year = Annotated[int, Field(strict=True, ge=2000, le=2100)]
Money = Annotated[
    Decimal,
    Field(ge=0, le=Decimal("999999999999.99"), decimal_places=2, allow_inf_nan=False),
    WithJsonSchema({"type": "number", "minimum": 0, "description": "Exact KES, at most two decimal places"}, mode="serialization"),
]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Request(Contract):
    userId: Identifier
    month: Month
    year: Year

    @field_validator("userId")
    @classmethod
    def nonblank_identity(cls, value):
        if not value.strip() or value != value.strip():
            raise ValueError("Use a nonblank ID without surrounding spaces")
        return value

    def key(self):
        return self.userId, self.month, self.year


class Item(Contract):
    type: Literal["review_category_budget"] = "review_category_budget"
    reason: Annotated[str, Field(min_length=1)]
    savingKes: Money
    targetId: Identifier


class Response(Contract):
    items: Annotated[list[Item], Field(max_length=3)]


class Feedback(Request):
    offerId: Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]
    expectedRevision: Annotated[int, Field(strict=True, ge=0)]
    action: Literal["shown", "accepted", "declined"]


class Budget(Request):
    targetId: Identifier
    category: Annotated[str, StringConstraints(min_length=1, max_length=80)]
    allocatedKes: Money
    actualKes: Money
    approved: bool = Field(strict=True)

    @field_validator("targetId", "category")
    @classmethod
    def nonblank_context(cls, value):
        if not value.strip() or value != value.strip():
            raise ValueError("Use nonblank budget identifiers and categories without surrounding spaces")
        return value

    @field_validator("allocatedKes", "actualKes", mode="before")
    @classmethod
    def exact_input_money(cls, value):
        if isinstance(value, (bool, float)):
            raise ValueError("Supply money as an exact decimal string or integer")
        return value


class SnapshotData(Contract):
    isSynthetic: Literal[True]
    budgets: list[Budget]

    @field_validator("isSynthetic", mode="before")
    @classmethod
    def explicitly_synthetic(cls, value):
        if value is not True:
            raise ValueError("An explicitly synthetic snapshot is required")
        return value
