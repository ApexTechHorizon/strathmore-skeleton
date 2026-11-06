from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import json

from fastapi.testclient import TestClient
import pytest

from app.feedback import FeedbackStore, StaleOffer
from app.main import ROOT, create_app
from app.schemas import Budget, Feedback, Request
from app.service import Snapshot, json_money

KEY = "synthetic-test-key-not-for-deployment-0000"
PERIOD = {"userId": "demo-household", "month": 6, "year": 2026}
HEADERS = {"Authorization": "Bearer " + KEY}


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(service_key=KEY, database_path=tmp_path / "feedback.sqlite3")) as client:
        yield client


def post(client, route="/recommendations", body=None):
    return client.post(route, json=PERIOD if body is None else body, headers=HEADERS)


def offers(client):
    response = post(client, "/recommendations/offers")
    assert response.status_code == 200
    return response.json()["offers"]


def decide(client, offer, action="accepted", **changes):
    return post(client, "/recommendations/feedback", {
        **PERIOD, "offerId": offer["offerId"], "expectedRevision": offer["revision"],
        "action": action, **changes,
    })


def metrics(client):
    return post(client, "/recommendations/metrics").json()


def write_snapshot(tmp_path, change):
    data = json.loads((ROOT / "data/demo.json").read_text())
    change(data)
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(data))
    return path


def test_health_demo_and_api_documentation(client):
    assert client.get("/health").json()["isSynthetic"] is True
    assert client.get("/demo").status_code == 200
    assert "Synthetic demonstration only" in client.get("/demo").text
    assert client.get("/demo/app.js").status_code == 200
    assert client.get("/docs").status_code == 200
    spec = client.get("/openapi.json").json()
    paths = spec["paths"]
    assert paths["/recommendations"]["post"]["security"] == [{"HTTPBearer": []}]
    assert spec["components"]["schemas"]["Item"]["properties"]["savingKes"]["type"] == "number"


def test_exact_contract_cap_ranking_and_baseline_number(client):
    response = post(client)
    assert response.status_code == 200
    assert set(response.json()) == {"items"}
    items = response.json()["items"]
    assert len(items) == 3
    assert [i["savingKes"] for i in items] == [1500, 600, 400]
    assert sum(i["savingKes"] for i in items) == 2500
    assert [i["targetId"] for i in items] == ["demo-entertainment", "demo-data", "demo-transport"]
    for item in items:
        assert set(item) == {"type", "reason", "savingKes", "targetId"}
        assert "retrospective" in item["reason"] and "if feasible" in item["reason"]
    assert post(client).content == response.content
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.parametrize("route", ["/recommendations", "/recommendations/offers", "/recommendations/feedback", "/recommendations/metrics"])
def test_protected_routes_reject_missing_wrong_and_unicode_keys(client, route):
    for headers in ({}, {"Authorization": "Bearer wrong"}, {"Authorization": "Basic invalid"}):
        response = client.post(route, json=PERIOD, headers=headers)
        assert response.status_code == 401
    # UTF-8 credential bytes are compared safely, never cast into ASCII.
    response = client.post(route, json=PERIOD, headers={"Authorization": b"Bearer \xc3\xa9"})
    assert response.status_code == 401


@pytest.mark.parametrize("body", [
    {}, [], None, {**PERIOD, "month": True}, {**PERIOD, "month": "6"},
    {**PERIOD, "month": 0}, {**PERIOD, "month": 13}, {**PERIOD, "year": False},
    {**PERIOD, "year": 2101}, {**PERIOD, "userId": " "}, {**PERIOD, "userId": " padded "},
    {**PERIOD, "userId": "x" * 129}, {**PERIOD, "extra": "do-not-echo-this"},
])
def test_invalid_requests_and_no_input_echo(client, body):
    response = client.post("/recommendations", json=body, headers=HEADERS)
    assert response.status_code == 422
    assert "do-not-echo-this" not in response.text


def test_malformed_json(client):
    response = client.post("/recommendations", content="{bad json", headers={**HEADERS, "Content-Type": "application/json"})
    assert response.status_code == 422


def test_household_period_scope_empty_and_missing(client):
    response = post(client, body={**PERIOD, "userId": "demo-other-household"})
    assert [i["targetId"] for i in response.json()["items"]] == ["demo-other-data"]
    assert post(client, body={**PERIOD, "month": 7}).json() == {"items": []}
    for body in ({**PERIOD, "month": 8}, {**PERIOD, "userId": "missing"}):
        assert post(client, body=body).status_code == 404
        assert post(client, "/recommendations/metrics", body).status_code == 404


def test_pending_essential_and_no_positive_gap_are_not_advice(tmp_path):
    def change(data):
        for row in data["budgets"]:
            if row["category"] in ("Entertainment", "Groceries", "Transport"):
                row["approved"] = False
            if row["category"] == "Airtime and Data":
                row["actualKes"] = row["allocatedKes"]
    source = Snapshot(write_snapshot(tmp_path, change))
    assert source.advice(Request(**PERIOD)).items == []


def test_equal_gaps_have_stable_target_order(tmp_path):
    def change(data):
        for row in data["budgets"]:
            row["allocatedKes"], row["actualKes"] = "100.01", "150.03"
    result = Snapshot(write_snapshot(tmp_path, change)).advice(Request(**PERIOD))
    assert [i.targetId for i in result.items] == ["demo-data", "demo-entertainment", "demo-groceries"]
    assert all(i.savingKes == Decimal("50.02") for i in result.items)


def test_large_money_stays_exact_json_number(tmp_path):
    def change(data):
        data["budgets"][0].update(actualKes="999999999999.99", allocatedKes="0.01")
    with TestClient(create_app(service_key=KEY, snapshot_path=write_snapshot(tmp_path, change),
                              database_path=tmp_path / "feedback.sqlite3")) as client:
        data = json.loads(post(client).content, parse_float=Decimal)
        assert data["items"][0]["savingKes"] == Decimal("999999999999.98")


@pytest.mark.parametrize("amount", ["NaN", "Infinity", "-1", "0.001", "1e30", True])
def test_invalid_snapshot_money_rejected(tmp_path, amount):
    with pytest.raises(ValueError):
        Snapshot(write_snapshot(tmp_path, lambda data: data["budgets"][0].update(actualKes=amount)))


def test_json_numeric_money_is_parsed_directly_as_decimal(tmp_path):
    source = Snapshot(write_snapshot(tmp_path, lambda data: data["budgets"][0].update(actualKes=6500.01)))
    assert source.advice(Request(**PERIOD)).items[0].savingKes == Decimal("1500.01")
    row = json.loads((ROOT / "data/demo.json").read_text())["budgets"][0]
    with pytest.raises(ValueError):
        Budget(**{**row, "actualKes": 6500.01})  # Already-converted Python floats are not exact inputs.


@pytest.mark.parametrize("change", [
    lambda d: d.update(isSynthetic=False),
    lambda d: d.update(isSynthetic=1),
    lambda d: d["budgets"].append(dict(d["budgets"][0])),
    lambda d: d["budgets"].append({**d["budgets"][0], "targetId": "different-target-same-category"}),
    lambda d: d["budgets"][0].update(targetId=" "),
    lambda d: d["budgets"][0].update(category=" "),
    lambda d: d["budgets"][0].update(approved="true"),
])
def test_bad_snapshot_fails_closed(tmp_path, change):
    with pytest.raises(ValueError):
        Snapshot(write_snapshot(tmp_path, change))


@pytest.mark.parametrize("key", ["", "short", "x" * 32 + " ", "é" * 32])
def test_service_requires_private_key_at_startup(tmp_path, key):
    with pytest.raises(ValueError), TestClient(create_app(service_key=key, database_path=tmp_path / "unused.sqlite3")):
        pass


def test_acceptance_has_explicit_display_unanswered_denominator_and_no_duplicates(client):
    assert metrics(client)["acceptRate"] is None
    first = offers(client)
    assert metrics(client)["shown"] == 0
    assert decide(client, first[0], "shown").status_code == 200
    assert metrics(client)["responded"] == 0
    assert decide(client, first[0]).status_code == 200
    assert decide(client, first[0]).status_code == 409
    assert [o["offerId"] for o in offers(client)] == [o["offerId"] for o in first]
    counts = metrics(client)
    assert (counts["delivered"], counts["shown"], counts["responded"], counts["accepted"]) == (3, 1, 1, 1)
    assert counts["acceptRate"] == 0.3333 and counts["shownAcceptRate"] == 1
    current = offers(client)[0]
    assert decide(client, current, "declined").status_code == 200
    assert metrics(client)["accepted"] == 0
    assert decide(client, first[0]).status_code == 409


def test_feedback_scope_validation_and_undelivered_offer(client):
    offer = offers(client)[0]
    assert decide(client, offer, userId="demo-other-household").status_code == 409
    assert decide(client, offer, month=7).status_code == 409
    for changes in ({"action": "invalid"}, {"expectedRevision": True}, {"offerId": "bad"}):
        assert decide(client, offer, **changes).status_code == 422
    assert metrics(client)["responded"] == 0
    # Knowing a content hash does not prove delivery.
    other = Request(userId="demo-other-household", month=6, year=2026)
    item = client.app.state.source.advice(other).items[0]
    body = {**other.model_dump(), "offerId": FeedbackStore.offer_id(other.key(), item),
            "expectedRevision": 0, "action": "accepted"}
    assert post(client, "/recommendations/feedback", body).status_code == 404


def test_database_survives_restart(tmp_path):
    path = tmp_path / "feedback.sqlite3"
    for iteration in range(2):
        with TestClient(create_app(service_key=KEY, database_path=path)) as client:
            current = offers(client)[0]
            if iteration == 0:
                assert decide(client, current).status_code == 200
            assert metrics(client)["accepted"] == 1
            assert metrics(client)["delivered"] == 3


def test_concurrent_delivery_deduplicates_and_decisions_conflict(tmp_path):
    source = Snapshot(ROOT / "data/demo.json")
    body = Request(**PERIOD)
    store = FeedbackStore(tmp_path / "feedback.sqlite3", source.identity)
    items = source.advice(body).items
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: store.issue(body.key(), items), range(12)))
    assert len({r[0]["offerId"] for r in results}) == 1
    assert store.metrics(body.key())["delivered"] == 3
    def decision(action):
        try:
            store.feedback(Feedback(**PERIOD, offerId=results[0][0]["offerId"], expectedRevision=0, action=action), items)
            return "ok"
        except StaleOffer:
            return "conflict"
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(decision, ("accepted", "declined"))) == ["conflict", "ok"]


def test_changed_offer_does_not_inherit_decisions_and_old_worker_is_blocked(tmp_path):
    path = tmp_path / "feedback.sqlite3"
    source = Snapshot(ROOT / "data/demo.json")
    body = Request(**PERIOD)
    old = FeedbackStore(path, source.identity)
    original_items = source.advice(body).items
    original = old.issue(body.key(), original_items)[0]
    old.feedback(Feedback(**PERIOD, offerId=original["offerId"], expectedRevision=0, action="accepted"), original_items)
    changed = Snapshot(write_snapshot(tmp_path, lambda d: d["budgets"][0].update(actualKes="6600.00")))
    new = FeedbackStore(path, changed.identity)
    replacement_items = changed.advice(body).items
    replacement = new.issue(body.key(), replacement_items)[0]
    assert replacement["offerId"] != original["offerId"]
    assert new.metrics(body.key())["delivered"] == 4
    with pytest.raises(StaleOffer):
        new.feedback(Feedback(**PERIOD, offerId=original["offerId"], expectedRevision=1, action="declined"), replacement_items)
    with pytest.raises(StaleOffer):
        old.issue(body.key(), original_items)
    with pytest.raises(StaleOffer):
        old.metrics(body.key())


def test_unrelated_snapshot_change_does_not_duplicate_offers(tmp_path):
    path = tmp_path / "feedback.sqlite3"
    body = Request(**PERIOD)
    source = Snapshot(ROOT / "data/demo.json")
    first = FeedbackStore(path, source.identity).issue(body.key(), source.advice(body).items)
    other = Snapshot(write_snapshot(tmp_path, lambda d: d["budgets"][-1].update(actualKes="1200.00")))
    store = FeedbackStore(path, other.identity)
    assert [o["offerId"] for o in store.issue(body.key(), other.advice(body).items)] == [o["offerId"] for o in first]
    assert store.metrics(body.key())["delivered"] == 3


def test_storage_failure_is_reported_without_internal_details(client, monkeypatch):
    import sqlite3
    def unavailable(*args):
        raise sqlite3.OperationalError("private-path-not-for-clients")
    monkeypatch.setattr(client.app.state.ledger, "issue", unavailable)
    response = post(client)
    assert response.status_code == 503
    assert "private-path" not in response.text


def test_json_serializer_rejects_nonfinite_and_keeps_decimal_numeric():
    assert json_money({"value": Decimal("50.02")}) == '{"value":50.02}'
    with pytest.raises(ValueError):
        json_money(Decimal("NaN"))
