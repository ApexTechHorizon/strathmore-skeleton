# chatbot/  —  integration point for U-CS 4

**AI Career Coaching Chatbot** · built by the assigned team

Answers easy questions with sources, hands over when it gets hard.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://chatbot.onrender.com  ->  chatbot/  ->  POST /chatbot/ask
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `CHATBOT_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `CHATBOT_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /chatbot/ask
  in : { question, userId }
  out: { answer, citations[], handover, handoverReason }
```

## Downstream

Changing this shape breaks: nobody directly

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `CHATBOT_SERVICE_URL`
2. The adapter in `chatbot.service.ts` already calls it — no code change needed
3. Hit `POST /chatbot/ask` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `chatbot.controller.ts` | Exposes the route on the platform |
| `chatbot.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `chatbot.module.ts` | Wires it into the app |
| `dto/chatbot.dto.ts` | The agreed request and response shapes |
