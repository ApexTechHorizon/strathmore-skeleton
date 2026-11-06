# spend-advisor — U-CS38

**Contributor: Eeshan Vaghjiani · Spendly**

Standalone spending-advice service: at most three specific actions, each with a
reason, exact KES reduction scenario and an existing budget target. Includes a
same-origin operator demo, persistent feedback and tests. Uses the starter's
FastAPI stack and adapts Spendly's existing advisor logic; it does not copy the
Flutter app or require either U-CS37 or U-CS46 to run. No other starter or
platform module is changed.

**Synthetic baseline, not a trained recommendation model.** Suggestions describe
returning to a previously approved allocation in a comparable period **if
feasible**. They are retrospective, not forecasts, affordability decisions,
guaranteed savings or evidence of real household adoption. Real data is rejected.

## Run locally

Python 3.11+ recommended. From `starters/spend-advisor`:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
$env:SPEND_ADVISOR_API_KEY = .venv/Scripts/python.exe -c "import secrets; print(secrets.token_hex(32))"
.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

On Linux/macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export SPEND_ADVISOR_API_KEY="$(.venv/bin/python -c 'import secrets; print(secrets.token_hex(32))')"
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- Health: <http://127.0.0.1:8000/health> (public, no key).
- Interactive contract: <http://127.0.0.1:8000/docs>; select **Authorize** and supply the key.
- Operator demo: <http://127.0.0.1:8000/demo>; use the same private key.
- Fixture: `demo-household`, June 2026. July returns an honest empty list.
- `demo-other-household`, June 2026, demonstrates separate household selection.

Keys must be private ASCII strings of at least 32 characters without whitespace.
Do not commit or log them. `.env.example` documents variables; the app deliberately
does **not** auto-load `.env`. The key in the operator page stays in page memory;
there is no local/session storage. Do not distribute a service key to real mobile
or web users. This demo is for a trusted staging operator only.

## Required contract (unchanged)

`POST /recommendations`, with `Authorization: Bearer <private-service-key>`:

```json
{"userId":"demo-household","month":6,"year":2026}
```

Returns exactly `{items:[{type,reason,savingKes,targetId}]}`. Example first item:

```json
{
  "type": "review_category_budget",
  "reason": "Review optional entertainment purchases and set a spending limit. In the synthetic 2026-06 snapshot, Entertainment spending was KES 6500.00 against an approved KES 5000.00 allocation. Returning to that allocation for a comparable period could reduce spending by KES 1500.00, if feasible. This is a retrospective planning scenario, not a forecast or guaranteed saving.",
  "savingKes": 1500.00,
  "targetId": "demo-entertainment"
}
```

`savingKes` is a JSON **number**, not a string. Money is parsed directly to
`Decimal`, checked for finite/nonnegative two-decimal KES, calculated and serialized
without converting through binary floats. The demo only rounds for display.

The baseline selects approved positive gaps in Entertainment, Groceries,
Transport, and Airtime and Data; it sorts largest first with target ID as a stable
tie-breaker and caps at three. Rent, medical, school fees and other categories
are not automatically treated as reducible. Nothing writes to source budgets.
The small fixture is hand-authored for this PR, not a Wasaa export.

Status codes: `401` missing/invalid key; `404` unknown household/period or
undelivered offer; `409` changed/withdrawn offer, stale revision or old worker;
`422` invalid input; `503` unavailable feedback storage. Known periods with no
qualifying opportunities return `200 {"items":[]}`. Error responses do not echo
financial inputs. Recommendation/feedback responses use `Cache-Control: no-store`.

## Feedback and acceptance demonstration (U-CS38-local extensions)

All three endpoints use the same service authorization. The required
`/recommendations` JSON is unchanged:

| Route | Request / result |
|---|---|
| `POST /recommendations/offers` | Same household/month/year; returns `{offers:[{offerId,revision,item}]}` |
| `POST /recommendations/feedback` | Household/month/year plus `offerId`, `expectedRevision`, `action` (`shown`, `accepted`, `declined`) |
| `POST /recommendations/metrics` | Household/month/year; returns counts, rates and definitions |

Use `/offers`, display the cards, then acknowledge `shown`. The supplied demo does
this and provides accept/decline buttons. A decision also acknowledges display.
Refetch offers after a decision to obtain the current revision. Replaying a stale
decision returns 409 rather than overwriting a later one.

- `acceptRate` = accepted unique offer versions / all unique delivered versions,
  including unanswered and superseded versions for that household's budget period.
- `shownAcceptRate` = accepted unique versions / explicitly shown versions.
- Rates are fractions (`0.3333` = 33.33%); empty denominators return `null`.
- Delivery means the service prepared a response, not proof of receipt/viewing.
- Identical deliveries do not inflate counts. Changed content gets a new offer
  identity and never inherits a previous decision. Historical versions remain.
- SQLite transactions serialize concurrent writes; state survives restart.

One accepted out of three delivered offers yields `0.3333` in the tests. **This
checks accounting, not measured human acceptance or actual money saved.** No
calls, events, auth assumptions or schema changes are made to U-CS46.

## Configuration and hosting

| Environment variable | Default |
|---|---|
| `SPEND_ADVISOR_API_KEY` | Required; no fallback key |
| `SPEND_ADVISOR_SNAPSHOT` | Included `data/demo.json` |
| `SPEND_ADVISOR_FEEDBACK_DB` | `var/feedback.sqlite3` |

Startup validates the entire immutable snapshot and initializes only the local
feedback database. Data must match the included JSON structure, contain
`isSynthetic:true`, exact KES amounts, unique targets, and unique categories per
household/month/year. Unapproved records never produce advice. The SHA-256 source
identity is tracked separately from offer content identity.

Run **one service instance** with a private persistent feedback volume. Deploy
one snapshot version at a time, replacing workers together. Old workers are
rejected after another version starts; an old process restarting can reactivate
its old snapshot. This is a small staging SQLite service, not a multi-host ledger.
Back up the feedback database and snapshot together; restore only into a stopped
instance. Rolling back code does not justify deleting recorded decisions.

```sh
docker build -t spend-advisor .
docker run --rm -p 127.0.0.1:8000:8000 --env SPEND_ADVISOR_API_KEY \
  -v spend-advisor-feedback:/app/var spend-advisor
```

The image runs as a non-root user. Use an HTTPS reverse proxy when hosting and
configure the public port through the container mapping or explicit uvicorn
`--port`; `PORT` is not automatically read by uvicorn. No hosted service is
created by this PR. `/health` is the liveness endpoint.

A service key authenticates the caller, **not household ownership**. The trusted
platform must authorize a household before forwarding its `userId`. Credential
transport and live data access require agreement; this PR deliberately operates
only on synthetic fixtures. Never put platform credentials or raw exports in Git.

## Tests and evidence

```powershell
.venv/Scripts/python.exe -m pytest tests -q
node --test tests/demo.test.cjs
```

Node 22+ is only needed for demo logic tests, not to run the service. GitHub Actions
runs these checks and a Docker build only for this starter's changes.

The main demo's four qualifying gaps rank to **KES 1,500 / 600 / 400**, totalling
**KES 2,500** for the three returned scenarios. These are fixture arithmetic,
not a measured economic benefit or a model quality score. Tests cover exact
contracts, invalid input, household/period selection, excluded spending, stable
ranking, exact large amounts, persistence, stale decisions and concurrency.

See [U-CS38 design and QA](docs/U-CS38.md) for the requirement/evidence map and
honest evaluation limitations. No forecast/anomaly model is promoted and no
claim is made that this baseline beats a learned recommendation system.
Actual local results and headless-browser checks are recorded in the
[6 November verification](docs/verification_2026_11_06.md).

## Provenance and PR boundary

Adapted from [Spendly's existing advisor](https://github.com/Eeshan-Vaghjiani/Spendly/tree/799fc94a2230d1f368293de3afbd9b2cf806f539/services/spend_advisor),
using the starter's FastAPI boundary instead of adding Flask. Research/model
accuracy, financial app features and the optional advisor are separate evidence.

Submitted by owner request as branch **U-CS38**, targeting the skeleton's `main`.
The skeleton's general instructions normally call for a standalone URL handoff;
this PR is for maintainer review and does not assume approval of a different
integration process. U-CS37, U-CS46, platform code and shared contracts are untouched.
