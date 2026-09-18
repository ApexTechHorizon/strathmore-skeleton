# career-path/  —  integration point for U-CS 1

**AI Career Path Recommendation** · built by the assigned team

What job could this person realistically do next.

---

## What this folder is

**Nothing is built here by the team.** They build and host their own service. This folder is
the adapter that calls their URL and exposes it on the platform.

```
their service                    this folder                the platform
https://career-path.onrender.com  ->  career-path/  ->  POST /career-path/paths
```

## What we need from them

| | |
|---|---|
| **Service URL** | A live endpoint that answers. Set as `CAREER_PATH_SERVICE_URL` |
| **Mini app URL** | Their demo page, so we can link to it. Set as `CAREER_PATH_APP_URL` |
| **Repo URL** | So the code can be read and, if it is good, lifted in |

## The contract

The shape is fixed. If it changes, both sides agree it and the Team Integration Map is reissued.

```
POST /career-path/paths
  in : { profile }
  out: { paths: [{ roleId, reachability, missingSkills[], reason }] }
```

## Downstream

Changing this shape breaks: micro-learning (U-CS 8)

---

## Wiring it in

1. Take the URL they give you, put it in `.env` as `CAREER_PATH_SERVICE_URL`
2. The adapter in `career-path.service.ts` already calls it — no code change needed
3. Hit `POST /career-path/paths` and confirm the shape comes back
4. If their service is down, the adapter returns a clear error rather than crashing the platform

## Files

| File | What it does |
|---|---|
| `career-path.controller.ts` | Exposes the route on the platform |
| `career-path.service.ts` | The adapter — calls their URL, checks the shape, handles failure |
| `career-path.module.ts` | Wires it into the app |
| `dto/career-path.dto.ts` | The agreed request and response shapes |
