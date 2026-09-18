# Backend API

> Replace this file with real instructions once you start building. Somebody who has just
> cloned this repo must be able to run it from here alone.

## Stack

NestJS, TypeScript, PostgreSQL, Prisma

## Setup

```bash
cp .env.example .env     # then fill in the values
npm install
npm run start:dev
```

## With Docker

```bash
docker build -t backend .
docker run -p 3000:3000 --env-file .env backend
```

## Environment variables

See `.env.example`. Never commit `.env`.

## Tests

```bash
# how to run them
```

## Deploy

Hosted at: <your live URL here>

See `documents/GIT_AND_DEPLOYMENT.md`.

## The integration layer

`src/modules/` is where student services get wired into the platform. **Students do not write
code in here.** They build and host their own service and hand over three URLs: the service,
their mini app, and their repo.

Each folder is an adapter that calls their URL. Set it in `.env`, and it works:

```
MATCHING_SERVICE_URL=https://matching.onrender.com
MATCHING_APP_URL=https://matching-demo.vercel.app
```

| Folder | Team | Their service does |
|---|---|---|
| `skills-gap/` | U-CS 3 | Skills gap and mentor trust scoring. **Upstream of two others** |
| `career-path/` | U-CS 1 | The realistic next role |
| `matching/` | U-CS 2 | Which mentor, within budget and availability |
| `chatbot/` | U-CS 4 | Answers easy questions, hands over when hard |
| `session-value/` | U-CS 5 | Will this session help, predicted beforehand |
| `pricing/` | U-CS 6 | A price both sides accept |
| `analytics/` | U-CS 7 | Cohort outcomes (unassigned — spare) |
| `micro-learning/` | U-CS 8 | The next lesson that closes a gap |

Until a URL is set, that adapter returns a clean `503` naming the missing variable — one late
team never takes the platform down. `GET /<module>/status` tells you whether a service is
configured and up.

See `src/modules/README.md` for the full map.
