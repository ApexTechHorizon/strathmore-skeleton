# micro-learning/  —  integration point for U-CS 8

**Micro-Learning Recommendation** · built by the assigned team

The next short lesson that closes a real gap and gets finished.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://micro-learning.onrender.com  ->  micro-learning/  ->  POST /micro-learning/next
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `MICRO_LEARNING_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `MICRO_LEARNING_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /micro-learning/next
  in : { userId, gap[] }
  out: { lessons: [{ lessonId, why, prereqsMet }] }
```

## Downstream

Changing this shape breaks: chatbot (U-CS 4)

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `MICRO_LEARNING_SERVICE_URL`
2. The adapter in `micro-learning.service.ts` already calls it — no code change needed
3. Hit `POST /micro-learning/next` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `micro-learning.controller.ts` | Exposes the route on the platform |
| `micro-learning.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `micro-learning.module.ts` | Wires it into the app |
| `dto/micro-learning.dto.ts` | The agreed request and response shapes |
