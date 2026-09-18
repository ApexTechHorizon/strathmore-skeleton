# pricing/  —  integration point for U-CS 6

**AI Pricing Optimization** · built by the assigned team

A price where the mentor still says yes and the student can still pay.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://pricing.onrender.com  ->  pricing/  ->  POST /pricing/price
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `PRICING_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `PRICING_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /pricing/price
  in : { mentorId }
  out: { min, max, comparables[], reason }
```

## Downstream

Changing this shape breaks: analytics (U-CS 7)

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `PRICING_SERVICE_URL`
2. The adapter in `pricing.service.ts` already calls it — no code change needed
3. Hit `POST /pricing/price` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `pricing.controller.ts` | Exposes the route on the platform |
| `pricing.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `pricing.module.ts` | Wires it into the app |
| `dto/pricing.dto.ts` | The agreed request and response shapes |
