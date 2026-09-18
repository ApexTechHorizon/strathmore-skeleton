# Modules — the integration layer

**No student writes code in here.**

Each team builds and hosts their own service, and gives us three things: a service URL, a mini
app URL, and a repo URL. Each folder below is an adapter that calls their service and exposes
it on the platform.

```
their service                       this folder              the platform
https://matching.onrender.com  ->   matching/          ->    POST /matching/match
their mini app                      linked from the platform, not proxied
```

## The eight integration points

| Folder | Team | What their service does | Built by |
|---|---|---|---|
| `skills-gap/` | U-CS 3 | What can this person do, what are they missing, can this mentor be trusted | the assigned team |
| `career-path/` | U-CS 1 | What job could they realistically do next | the assigned team |
| `matching/` | U-CS 2 | Which mentor, within budget and availability | the assigned team |
| `chatbot/` | U-CS 4 | Answers easy questions, hands over when it gets hard | the assigned team |
| `session-value/` | U-CS 5 | Predicts whether a session will help, before it happens | the assigned team |
| `pricing/` | U-CS 6 | A price both sides say yes to | the assigned team |
| `analytics/` | U-CS 7 | What a cohort did and whether it mattered | unassigned — spare |
| `micro-learning/` | U-CS 8 | The next lesson that closes a real gap | the assigned team |

## How the services call each other

```
skills-gap  ->  career-path  ->  micro-learning  ->  chatbot
            ->  matching     ->  session-value   ->  analytics
                             ->  pricing         ->  analytics
```

**`skills-gap` is upstream of two others.** If that team is late, two more are blocked.

## Wiring a team in

1. They send a service URL, a mini app URL and a repo URL
2. Put the service URL in `.env` — for example `MATCHING_SERVICE_URL=https://...`
3. Nothing else to change. The adapter already calls it
4. Check it: `GET /matching/status` reports whether their service is configured and up
5. Link their mini app from the platform using `MATCHING_APP_URL`

Until a URL is set, that adapter returns a clean `503` naming the missing variable. One team
being late never takes the platform down.

## Before a demo

```bash
for m in skills-gap career-path matching chatbot session-value pricing analytics micro-learning; do
  echo -n "$m: "; curl -s localhost:3000/$m/status
  echo
done
```

Free hosting sleeps after inactivity, so the first call can take thirty seconds. Run this a few
minutes before anyone looks.

## Why it is built this way

- **Their work stays theirs.** Own repo, own deploy, own history. Nothing to merge.
- **One broken service cannot break the platform.** Failure is contained to one adapter.
- **The contract is the only coupling.** What happens behind their URL is entirely up to them,
  in any language.
- **Lifting good work in later is easy.** If a service is good enough to bring in-house, the
  adapter is the seam to replace.
