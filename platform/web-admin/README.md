# Admin Console

> Replace this file with real instructions once you start building. Somebody who has just
> cloned this repo must be able to run it from here alone.

## Stack

Next.js, TypeScript, Tailwind

## Setup

```bash
cp .env.example .env     # then fill in the values
npm install
npm run dev
```

## With Docker

```bash
docker build -t web-admin .
docker run -p 3000:3000 --env-file .env web-admin
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
