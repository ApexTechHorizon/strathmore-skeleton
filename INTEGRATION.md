# Getting the data, and getting your work connected

Two questions everyone is asking. Both answers are shorter than you expect.

---

## 1. There is no pull request

You do not merge your code into the platform. You never touch the platform
repository at all.

Your service runs on its own, wherever you host it. The platform calls it over
HTTP. So the handover is a **URL**, not a merge:

1. Build and deploy your service.
2. Send Benjamin the URL.
3. He sets one environment variable and your service is live in the platform.

That is the whole integration. Keep working in your own repository, with your
own issues, branches and milestones — that is also the work your examiner
grades, so it should stay yours and stay busy.

The adapter for your use case **already exists** on the platform side. It is
waiting for a URL. Until one is set it returns a clean 503 naming the missing
variable, so a late team never takes anything else down.

Check them all: `GET /api/v1/integrations/status`

### What has to stay fixed

Everything inside your service can change as often as you like. Two things
cannot change without telling everyone:

- the **route** — the path the platform calls
- the **shape** — the JSON in and the JSON out

Those are in the table at the bottom. If you need a different shape, agree it
with the team upstream and downstream of you first, then tell Benjamin so the
integration map gets reissued.

You also need a `GET /health` that returns 200. That is how the platform knows
you are up.

### Free hosting sleeps

Render, Railway and the rest put a free service to sleep after idle time. The
first call then takes up to 30 seconds. The platform allows for that — the
timeout is 30s — but do not be surprised by it in a demo.

---

## 2. The data is already there

A staging database is filled with a synthetic world: households, their
families, their monthly budgets, their bookings, and every shilling that moved.
You do not have to invent a dataset.

**All of it is synthetic.** Say so in your report. Nobody loses marks for honest
synthetic data; presenting it as real is a different matter.

### Option A — the API

Log in and query it. Same data the platform serves, same ids.

```
POST https://api-wasaa-lifestyle.webmasterskenya.com/api/v1/auth/login
     { "email": "user@wasaalifestyle.com", "password": "User123!" }
```

Use the `accessToken` it returns as `Authorization: Bearer <token>`.
Browsable route list: `/docs`

### Option B — CSV, for training a model

Nobody trains over HTTP. Ask Benjamin for the export and you get flat files
with the same ids the API serves, so a model fitted offline lines up with the
platform when your service goes live.

| file | what it is |
|---|---|
| `households.csv` | one row per household; `user_profile_id` joins everywhere |
| `dependants.csv` | spouse, child, parent, sibling, extended family |
| `providers.csv` / `services.csv` | the supply side |
| `bookings.csv` | one row per booking, with the outcome and a `did_not_show` label |
| `reviews.csv` | only for jobs that actually happened |
| `budget_categories.csv` | monthly budget per household per category |
| `spending_records.csv` | individual spend events inside those categories |
| `transactions.csv` / `ledger_entries.csv` | every money movement, double-entry |

Every file joins on `user_profile_id`, `provider_id`, `service_id`,
`booking_id` or `transaction_id`. That is deliberate: it is what lets team 46
aggregate what teams 37 to 43 produce.

### Which files you need

| use case | start with |
|---|---|
| U-CS 37 budget-forecast | `budget_categories`, `spending_records`, `households` |
| U-CS 38 spend-advisor | those three, plus `bookings` |
| U-CS 39 marketplace-search | `services`, `providers`, `reviews` |
| U-CS 40 provider-match | `bookings`, `providers`, `reviews` |
| U-CS 41 scheduling | `bookings` — the `did_not_show` label is here |
| U-CS 42 wallet-checks | `transactions`, `ledger_entries` |
| U-CS 43 dependant-costs | `dependants`, `budget_categories`, `spending_records` |
| U-CS 46 ops-metrics | all of them |

### Two traps worth knowing

**Leakage.** In `bookings.csv`, `booking_status`, `payment_status`,
`completed_at` and `cancelled_at` only exist *because* the appointment already
happened. Feed any of them to a model predicting `did_not_show` and you will
see a near-perfect score in your notebook and nothing in production.

**Time.** Split by `created_at`, not at random. A random split lets the model
see a household's future while predicting its past, which it can never do on a
live booking.

### The money balances

Every transaction has paired ledger entries whose debits equal its credits, and
each entry carries the running balance of its account in date order. One
balance is negative on purpose — the `SYSTEM` `AVAILABLE` account, which is
where deposits from M-Pesa are debited, so it holds the negative of the float
the platform is carrying. Any *other* negative balance is a bug; say so.

---

## The contracts

Call your service by its slug everywhere — your repository name, your URL, your
route, and the variable Benjamin sets.

| use case | slug | your endpoint | in | out |
|---|---|---|---|---|
| U-CS 37 | `budget-forecast` | `POST /forecast` | `{ userId, month, year }` | `{ estimatedTotal, breakdown{}, confidence, riskFlag }` |
| U-CS 38 | `spend-advisor` | `POST /recommendations` | `{ userId, month, year }` | `{ items:[{type,reason,savingKes,targetId}] }` |
| U-CS 39 | `marketplace-search` | `POST /search` | `{ q, categoryId, lat, lng }` | `{ results:[{serviceId,score,why}] }` |
| U-CS 40 | `provider-match` | `POST /match` | `{ userId, categoryId, lat, lng }` | `{ providers:[{providerId,score,reason}] }` |
| U-CS 41 | `scheduling` | `POST /noshow/predict` | `{ bookingId }` | `{ probability, factors[] }` |
| U-CS 42 | `wallet-checks` | `POST /ledger/verify` | `{ from, to }` | `{ balanced, discrepancies[] }` |
| U-CS 43 | `dependant-costs` | `POST /projection` | `{ dependantId }` | `{ oneYear, fiveYear, tenYear, peakYear, breakdown{}, assumptions[] }` |
| U-CS 44 | `access-pass-ai` | `POST /scan/anomaly` | `{ passId }` | `{ risk, why }` |
| U-CS 45 | `emergency-triage` | `POST /triage` | `{ type, context, geo }` | `{ priority, routeTo, escalateAfterMins, fallbackChannel }` |
| U-CS 46 | `ops-metrics` | `POST /metrics` | `{ from, to }` | `{ metrics:[{name,value,definition,decisionItSupports}] }` |

Plus `GET /health` on every service.

---

## If you are stuck

Ask. A question on the day it appears costs you ten minutes; the same question
in week four costs you the demo.
