# skills-gap/  —  integration point for U-CS 3

**Skills Gap & Trust Scoring** · built by the assigned team

What can this person do, what are they missing, and can this mentor be trusted.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://skills-gap.onrender.com  ->  skills-gap/  ->  POST /skills-gap/gap
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `SKILLS_GAP_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `SKILLS_GAP_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /skills-gap/gap
  in : { profile, targetRole }
  out: { have[], missing[{skill, confidence}], readiness }
```

## Downstream

Changing this shape breaks: career-path (U-CS 1) and micro-learning (U-CS 8)

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `SKILLS_GAP_SERVICE_URL`
2. The adapter in `skills-gap.service.ts` already calls it — no code change needed
3. Hit `POST /skills-gap/gap` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `skills-gap.controller.ts` | Exposes the route on the platform |
| `skills-gap.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `skills-gap.module.ts` | Wires it into the app |
| `dto/skills-gap.dto.ts` | The agreed request and response shapes |
