# ML Service

**This is where most use cases live.** One small web service with one endpoint that other
teams call.

## Stack

Python 3.11, FastAPI, scikit-learn, pandas

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs — FastAPI generates interactive API docs for free. Use them to
test your endpoint without writing a client.

## Your contract

Replace the placeholder in `app/main.py` with the endpoint from your card in the Team
Integration Map. Keep the shape exactly as agreed — other teams depend on it.

```
POST /your-endpoint
  in : { ... }
  out: { ... }
```

If the shape needs to change, agree it with the teams on the other side first, then tell
Benjamin so the map gets reissued.

## The order of work

1. Baseline — the dumbest thing that works. Measure it. **Write the number down.**
2. Decide the metric and hold out test data.
3. Build the real model. Show it beats the baseline.
4. Deploy. Share the URL.

## With Docker

```bash
docker build -t ml-service .
docker run -p 8000:8000 --env-file .env ml-service
curl http://localhost:8000/health
```

## Deploy

Render, Railway, Fly.io or Hugging Face Spaces. All read the Dockerfile.

Hosted at: <your live URL here>
