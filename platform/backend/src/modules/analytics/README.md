# analytics/  —  integration point for U-CS 7

**Institution Impact Analytics** · built by the assigned team

What a sponsored cohort did, and whether anything changed.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://analytics.onrender.com  ->  analytics/  ->  POST /analytics/cohort
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `ANALYTICS_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `ANALYTICS_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /analytics/cohort
  in : { cohortId }
  out: { engagement{}, progression{}, outcomes{}, caveats[] }
```

## Downstream

Changing this shape breaks: nobody

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `ANALYTICS_SERVICE_URL`
2. The adapter in `analytics.service.ts` already calls it — no code change needed
3. Hit `POST /analytics/cohort` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `analytics.controller.ts` | Exposes the route on the platform |
| `analytics.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `analytics.module.ts` | Wires it into the app |
| `dto/analytics.dto.ts` | The agreed request and response shapes |
