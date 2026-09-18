# Project Skeleton

Starting point for Strathmore use-case projects on **Wasaa Lifestyle** and **Career Mentor OS**.

Copy this whole folder, rename it to your project, and start filling it in.

```bash
cp -r strathmore-skeleton my-project
cd my-project
```

## What is in here

| Folder | What it is for |
|---|---|
| `documents/` | The write-up. Start here, before you write code. See `documents/00-START-HERE.md` |
| `ml-service/` | Your model, served over HTTP. **Most of you live here** |
| `backend/` | The API server, if your use case needs one |
| `web-client/` | The user-facing web app |
| `web-admin/` | The internal console |
| `flutter/` | The mobile app |

Every code folder contains the same five files:

| File | What it does |
|---|---|
| `Dockerfile` | Packages the app so it runs the same everywhere — on your laptop and on the host |
| `.dockerignore` | Keeps junk out of the Docker image (node_modules, .env, .git) |
| `.gitignore` | Keeps secrets, dependencies and big files out of git. **Read it before your first commit** |
| `.env.example` | The variable names your app needs. Copy to `.env` and fill in. Never commit `.env` |
| `README.md` | How to run this folder. Replace it with real instructions as you build |

`ml-service/` also has `app/main.py` — a working FastAPI service with a `/health` endpoint and a
placeholder that returns a constant, labelled `baseline: constant prediction`. Replace the
placeholder with the endpoint from your card.

**You will not need all of these.** Most use cases are one service plus a small page to demo it.
Delete the folders you are not using — an empty folder in a repo is noise.

## Every folder is its own repository

`backend`, `ml-service`, `web-client`, `web-admin` and `flutter` each get their own GitHub repo
and their own deploy. They are separate things with separate lifecycles.

Each one already has a `Dockerfile`, a `.gitignore` and a `.env.example`, so it can be built and
hosted from day one.

See `documents/GIT_AND_DEPLOYMENT.md` for the exact commands.

## The order of work

1. **Fill in the Concept Note.** If you cannot, you do not understand the problem yet.
2. **Write the contract** — the endpoint, what goes in, what comes out. It is on your card in
   the Team Integration Map.
3. **Build the baseline.** The dumbest version that works. Write down its number.
4. **Decide how you measure success**, and what data you hold back to test on.
5. **Then** build the clever version, and show it beats the baseline.
6. **Then** deploy it and give me the URL.

Most teams want to start at step 5. That is the mistake that costs the most marks.

## What you hand in

- A GitHub repo URL for each folder you used
- A live URL for your service
- A `README.md` in each repo explaining how to run it
- The `documents/` folder, filled in

## Rules that are not negotiable

- **No secrets in git.** No `.env`, no keys, no keystores. Commit `.env.example` instead.
- **Staging only.** No production data, no real user records, no live M-Pesa.
- **Label synthetic data as synthetic** — in the code and in the report.
- **Money is decimal, never float.**
- If you find a real bug in our platform, tell me the same day.

## Quick start per folder

```bash
# ml-service (Python)
cd ml-service && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
curl http://localhost:8000/health

# any folder, with Docker
docker build -t my-service . && docker run -p 8000:8000 my-service
```
