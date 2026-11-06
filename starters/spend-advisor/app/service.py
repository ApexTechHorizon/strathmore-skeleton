"""Spendly's transparent retrospective baseline, adapted to the starter contract.

No forecast/model calls, live data, or invented achievable savings. Source:
Eeshan-Vaghjiani/Spendly services/spend_advisor, main 799fc94a.
"""
from decimal import Decimal
import hashlib
import json
from pathlib import Path

from pydantic import BaseModel

from app.schemas import Item, Request, Response, SnapshotData

ACTIONS = {
    "Entertainment": "Review optional entertainment purchases and set a spending limit",
    "Groceries": "Review grocery purchases and plan a shopping list within the allocation",
    "Airtime and Data": "Review usage and compare airtime and data packages",
    "Transport": "Review optional trips and compare lower-cost transport options",
}


def json_money(value):
    """Exact JSON numeric tokens; Pydantic's default Decimal encoding is a string."""
    if isinstance(value, BaseModel):
        value = value.model_dump()
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("Nonfinite money")
        return format(value, "f")
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k) + ":" + json_money(v) for k, v in value.items()) + "}"
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(map(json_money, value)) + "]"
    return json.dumps(value, allow_nan=False)


class Snapshot:
    def __init__(self, path):
        payload = Path(path).read_bytes()
        # Decimal parsing avoids binary-float conversion even for JSON numeric inputs.
        data = SnapshotData.model_validate(json.loads(payload, parse_float=Decimal))
        self.identity = hashlib.sha256(payload).hexdigest()
        self.by_period = {}
        targets, categories = set(), set()
        for budget in data.budgets:
            category_key = (*budget.key(), budget.category)
            if budget.targetId in targets or category_key in categories:
                raise ValueError("Duplicate budget target or household-period category")
            targets.add(budget.targetId)
            categories.add(category_key)
            self.by_period.setdefault(budget.key(), []).append(budget)

    def advice(self, body: Request) -> Response:
        rows = self.by_period.get(body.key())
        if rows is None:
            raise LookupError("No synthetic snapshot for this household and period")
        items = []
        for row in rows:
            if not row.approved or row.category not in ACTIONS or row.actualKes <= row.allocatedKes:
                continue
            difference = row.actualKes - row.allocatedKes
            items.append(Item(
                targetId=row.targetId,
                savingKes=difference,
                reason=(f"{ACTIONS[row.category]}. In the synthetic {body.year}-{body.month:02d} "
                        f"snapshot, {row.category} spending was KES {row.actualKes:.2f} against an "
                        f"approved KES {row.allocatedKes:.2f} allocation. Returning to that allocation "
                        f"for a comparable period could reduce spending by KES {difference:.2f}, if feasible. "
                        "This is a retrospective planning scenario, not a forecast or guaranteed saving."),
            ))
        return Response(items=sorted(items, key=lambda item: (-item.savingKes, item.targetId))[:3])
