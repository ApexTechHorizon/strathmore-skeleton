# U-CS38 verification — 6 November 2026

Scope: the standalone starter and its synthetic fixtures, on branch `U-CS38`.
No other use-case service, live account, Wasaa API, production database, model
artifact, training notebook or Spendly application data was changed or queried.

## Automated local checks

Environment: Windows, isolated Python3.13 virtual environment, Node24.14.1;
starter-pinned FastAPI0.115.0 / Pydantic2.9.2 / pytest8.3.3.

- `python -m pytest tests -q`: **50 passed**, zero failed. One dependency warning
  about Starlette's deprecated AnyIO portal type alias; no application warning.
- `node --test tests/demo.test.cjs`: **3 passed**, zero failed.
- `python -m pip check`: no broken requirements.
- Whitespace/diff scope checked before publication.

Python tests run real local SQLite transactions with synthetic fixtures, including
threaded competing decisions and delivery retries. FastAPI route tests use
TestClient, not the hosted platform. Node tests simulate a minimal DOM, not a
browser. None of these establish genuine human adoption or achieved savings.

## Actual HTTP and headless-browser acceptance

A separate local uvicorn process used a freshly generated private key and an
isolated temporary SQLite file. An existing Microsoft Edge executable was launched
headlessly with a new temporary profile, no personal profile or signed-in account.
The check used loopback HTTP and the browser's loopback debugging connection.
No key, financial input or screenshot was printed or published.

Passed checkpoints:

1. Health responds; invalid key returns401 over a real HTTP socket.
2. `/recommendations` returns reductions1500/600/400 for the synthetic June fixture.
3. `/demo` loads in Edge and displays three cards, including KES1500.00.
4. Rendering acknowledges three shown offers.
5. Clicking Accept records one acceptance; displayed `acceptRate` is0.3333.
6. Clicking Decline on the refreshed offer records zero accepted without a stale
   revision overwrite.
7. July's known no-opportunity period displays the empty state.
8. A wrong key displays the error state and removes old cards.

All launched browser/server processes were stopped. Disposable synthetic SQLite
and browser-profile artifacts were retained in the approved local temporary area,
outside Git; they contain no real-user data. No public URL was started.

## Not established

- Docker is installed but its Linux engine was unavailable locally; no local
  image build/run is claimed. The scoped CI workflow includes an image build.
- The container's Python3.11/Linux execution and CI results must be read from the
  actual PR checks, not inferred from the Windows/Python3.13 run.
- No external-team integration, public hosting, real-user acceptance study,
  chronological recommendation-model evaluation, screen-reader audit or
  institutional approval was performed. These are not relabelled as passed.

The functional U-CS38 implementation and synthetic acceptance mechanism are
delivered for review; broader deployment/research acceptance remains distinct.
