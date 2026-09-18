# session-value/  —  integration point for U-CS 5

**Session Effectiveness Predictor** · built by the assigned team

Predicts before a session whether it will help.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://session-value.onrender.com  ->  session-value/  ->  POST /session-value/predict
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `SESSION_VALUE_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `SESSION_VALUE_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /session-value/predict
  in : { menteeId, mentorId, leadTimeHours, hasAgenda, isFirstSession }
  out: { probability, factors[], suggestedIntervention }
```

## Downstream

Changing this shape breaks: analytics (U-CS 7)

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `SESSION_VALUE_SERVICE_URL`
2. The adapter in `session-value.service.ts` already calls it — no code change needed
3. Hit `POST /session-value/predict` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `session-value.controller.ts` | Exposes the route on the platform |
| `session-value.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `session-value.module.ts` | Wires it into the app |
| `dto/session-value.dto.ts` | The agreed request and response shapes |
