# matching/  —  integration point for U-CS 2

**Intelligent Mentor Matching** · built by the assigned team

Which mentor, within budget, availability and language.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://matching.onrender.com  ->  matching/  ->  POST /matching/match
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `MATCHING_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `MATCHING_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /matching/match
  in : { menteeId, needs: { budgetMax, timeframeWeeks, language } }
  out: { mentors: [{ mentorId, score, reason }] }
```

## Downstream

Changing this shape breaks: session-value (U-CS 5), pricing (U-CS 6), analytics (U-CS 7)

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `MATCHING_SERVICE_URL`
2. The adapter in `matching.service.ts` already calls it — no code change needed
3. Hit `POST /matching/match` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `matching.controller.ts` | Exposes the route on the platform |
| `matching.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `matching.module.ts` | Wires it into the app |
| `dto/matching.dto.ts` | The agreed request and response shapes |
