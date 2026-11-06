"""Standalone U-CS38 service. No calls or changes to U-CS37/U-CS46."""
from contextlib import asynccontextmanager
import hmac
import os
from pathlib import Path
import sqlite3

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, Response as HttpResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.feedback import FeedbackStore, StaleOffer
from app.schemas import Feedback, Request, Response
from app.service import Snapshot, json_money

ROOT = Path(__file__).resolve().parent.parent
bearer = HTTPBearer(auto_error=False)


class DecimalResponse(HttpResponse):
    media_type = "application/json"

    def render(self, content):
        return json_money(content).encode("utf-8")


def create_app(*, snapshot_path=None, database_path=None, service_key=None):
    @asynccontextmanager
    async def lifespan(app):
        key = service_key if service_key is not None else os.environ.get("SPEND_ADVISOR_API_KEY", "")
        if len(key) < 32 or not key.isascii() or any(c.isspace() for c in key):
            raise ValueError("Set SPEND_ADVISOR_API_KEY to a private ASCII key of at least 32 characters, without spaces")
        app.state.service_key = key
        app.state.source = Snapshot(snapshot_path or os.environ.get("SPEND_ADVISOR_SNAPSHOT", ROOT / "data/demo.json"))
        app.state.ledger = FeedbackStore(
            database_path or os.environ.get("SPEND_ADVISOR_FEEDBACK_DB", ROOT / "var/feedback.sqlite3"),
            app.state.source.identity,
        )
        yield

    app = FastAPI(title="U-CS 38 — spend-advisor", version="1.0.0", lifespan=lifespan)

    def authenticate(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if credentials is None or not hmac.compare_digest(
            credentials.credentials.encode("utf-8"), app.state.service_key.encode("ascii")
        ):
            raise HTTPException(401, "Unauthorized", headers={"WWW-Authenticate": "Bearer"})

    @app.middleware("http")
    async def no_cache(request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, error):
        # Never echo financial input or arbitrary extra fields in validation errors.
        return DecimalResponse({"detail": [{"loc": list(e["loc"]), "type": e["type"]} for e in error.errors()]}, status_code=422)

    @app.exception_handler(StaleOffer)
    async def stale_offer(request, error):
        return DecimalResponse({"detail": "Snapshot or offer changed; refresh before retrying"}, status_code=409)

    @app.exception_handler(sqlite3.OperationalError)
    async def unavailable_storage(request, error):
        return DecimalResponse({"detail": "Feedback storage unavailable; retry later"}, status_code=503)

    def advice(body):
        try:
            return app.state.source.advice(body)
        except LookupError:
            raise HTTPException(404, "No synthetic snapshot for this household and period") from None

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "spend-advisor", "isSynthetic": True,
                "method": "retrospective-approved-budget-gap-v1"}

    @app.get("/demo", include_in_schema=False)
    def demo():
        return FileResponse(ROOT / "demo/index.html")

    @app.get("/demo/app.js", include_in_schema=False)
    def demo_script():
        return FileResponse(ROOT / "demo/app.js", media_type="text/javascript")

    @app.post("/recommendations", response_model=Response, dependencies=[Depends(authenticate)])
    def recommendations(body: Request):
        result = advice(body)
        app.state.ledger.issue(body.key(), result.items)
        return DecimalResponse(result)

    @app.post("/recommendations/offers", dependencies=[Depends(authenticate)])
    def offers(body: Request):
        result = advice(body)
        return DecimalResponse({"offers": app.state.ledger.issue(body.key(), result.items)})

    @app.post("/recommendations/feedback", dependencies=[Depends(authenticate)])
    def feedback(body: Feedback):
        try:
            app.state.ledger.feedback(body, advice(body).items)
        except LookupError:
            raise HTTPException(404, "Offer has not been delivered") from None
        return {"recorded": True}

    @app.post("/recommendations/metrics", dependencies=[Depends(authenticate)])
    def metrics(body: Request):
        advice(body)  # Unknown households/periods are never invented as empty histories.
        return DecimalResponse(app.state.ledger.metrics(body.key()))

    return app


app = create_app()
