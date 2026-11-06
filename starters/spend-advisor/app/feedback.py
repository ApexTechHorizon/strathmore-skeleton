"""Spendly's versioned SQLite feedback accounting, scoped to U-CS38 only."""
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sqlite3

from app.service import json_money


class StaleOffer(Exception):
    pass


class FeedbackStore:
    def __init__(self, path, source_identity):
        self.path = Path(path)
        self.source_identity = source_identity
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS offers (
                    offer_id TEXT PRIMARY KEY,
                    owner TEXT NOT NULL, month INTEGER NOT NULL, year INTEGER NOT NULL,
                    payload TEXT NOT NULL, first_delivered TEXT NOT NULL,
                    shown_at TEXT, decision INTEGER CHECK(decision IN (0,1)),
                    active INTEGER NOT NULL CHECK(active IN (0,1)),
                    revision INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS offers_period ON offers(owner, month, year);
                CREATE TABLE IF NOT EXISTS source_state (
                    id INTEGER PRIMARY KEY CHECK(id=1), identity TEXT NOT NULL
                );
            """)
            # shortcut: one snapshot per deployment; coordinate restarts before supporting rolling updates.
            db.execute("INSERT INTO source_state VALUES (1,?) ON CONFLICT(id) DO UPDATE SET identity=excluded.identity",
                       (source_identity,))

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def check_source(self, db):
        current = db.execute("SELECT identity FROM source_state WHERE id=1").fetchone()
        if current["identity"] != self.source_identity:
            raise StaleOffer("Snapshot changed; restart this worker")

    @staticmethod
    def offer_id(key, item):
        identity = json.dumps([*key, json_money(item)], separators=(",", ":"))
        return hashlib.sha256(identity.encode()).hexdigest()

    def issue(self, key, items):
        offers = []
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self.check_source(db)
            db.execute("UPDATE offers SET active=0 WHERE owner=? AND month=? AND year=?", key)
            for item in items:
                offer_id = self.offer_id(key, item)
                db.execute("""INSERT INTO offers
                    (offer_id,owner,month,year,payload,first_delivered,active)
                    VALUES (?,?,?,?,?,?,1)
                    ON CONFLICT(offer_id) DO UPDATE SET active=1""",
                    (offer_id, *key, json_money(item), datetime.now(timezone.utc).isoformat()))
                revision = db.execute("SELECT revision FROM offers WHERE offer_id=?", (offer_id,)).fetchone()["revision"]
                offers.append({"offerId": offer_id, "revision": revision, "item": item})
        return offers

    def feedback(self, body, current_items):
        if body.offerId not in {self.offer_id(body.key(), item) for item in current_items}:
            raise StaleOffer("Offer is not current for this household and period")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self.check_source(db)
            offer = db.execute("SELECT active,revision,decision FROM offers WHERE offer_id=? AND owner=? AND month=? AND year=?",
                               (body.offerId, *body.key())).fetchone()
            if offer is None:
                raise LookupError("Offer has not been delivered")
            if not offer["active"]:
                raise StaleOffer("Offer was replaced or withdrawn")
            if body.action != "shown" and offer["revision"] != body.expectedRevision:
                raise StaleOffer("Decision changed; refresh offers before retrying")
            db.execute("UPDATE offers SET shown_at=COALESCE(shown_at,?) WHERE offer_id=?",
                       (datetime.now(timezone.utc).isoformat(), body.offerId))
            if body.action != "shown":
                accepted = int(body.action == "accepted")
                db.execute("""UPDATE offers SET decision=?,revision=revision+1
                    WHERE offer_id=? AND (decision IS NULL OR decision!=?)""",
                    (accepted, body.offerId, accepted))

    def metrics(self, key):
        with self.connect() as db:
            self.check_source(db)
            counts = dict(db.execute("""SELECT COUNT(*) AS delivered,
                COALESCE(SUM(shown_at IS NOT NULL),0) AS shown,
                COALESCE(SUM(decision IS NOT NULL),0) AS responded,
                COALESCE(SUM(decision=1),0) AS accepted,
                COALESCE(SUM(active),0) AS active
                FROM offers WHERE owner=? AND month=? AND year=?""", key).fetchone())
        def rate(denominator):
            return (Decimal(counts["accepted"]) / Decimal(denominator)).quantize(Decimal(".0001")) if denominator else None
        return {
            **counts, "acceptRate": rate(counts["delivered"]), "shownAcceptRate": rate(counts["shown"]),
            "definition": "Accepted unique offer versions / all unique delivered versions for this household and budget month/year; unanswered and superseded versions remain in the denominator.",
            "deliveryDefinition": "Prepared by the service, not proof of receipt or display.",
            "shownDefinition": "Explicit display acknowledgement or decision.",
            "isSynthetic": True,
        }
