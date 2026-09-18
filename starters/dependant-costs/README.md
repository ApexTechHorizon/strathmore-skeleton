# dependant-costs  —  U-CS 43

**Dependants Budget Management** · Wasaa Lifestyle

What supporting a child or relative costs over one, five and ten years, and which year is worst.

---

## Your contract

This is the shape the rest of the system expects. Agree any change with the teams below,
then tell Benjamin so the Team Integration Map gets reissued.

```
POST /projection
  in : { "dependantId": "..." }
  out: { "oneYear": 0, "fiveYear": 0, "tenYear": 0, "peakYear": 2036, "breakdown": {}, "assumptions": [] }
```

**Call it `dependant-costs` everywhere** — your repo name, your service URL, your route, and the
variable Benjamin sets when integrating you: `DEPENDANT_COSTS_SERVICE_URL`

## Who you depend on

U-CS 37 (budget-forecast) for the household cost model.

## Who depends on you

U-CS 46 (ops-metrics)

## Done when

Projections come with a stated range and assumptions, plus a note on handling children’s data.

---

## Run it

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open <http://localhost:8000/docs> — FastAPI gives you interactive API docs for free, so you can
test your endpoint without writing a client. Open `demo/index.html` for the mini app.

```bash
pytest -q                 # the contract test
docker build -t dependant-costs . && docker run -p 8000:8000 dependant-costs
```

## The order of work

1. **Baseline.** The dumbest thing that works, returned from `app/service.py`. Measure it and
   **write the number down.** You are not allowed to build a model before this exists.
2. **Evaluation.** Pick your metric. Split your data **by time**, not at random, and hold the
   last part back.
3. **Model.** Build the real thing. Show it beats the baseline.
4. **Integration.** Keep the contract identical while the inside changes completely. Deploy it,
   send Benjamin the URL.

## What you hand in

- This repo, on GitHub, with Benjamin added as a collaborator
- A live URL that answers
- The filled-in documents (templates are in the `documents/` folder of the skeleton repo)
- A README a stranger could run this from

## Rules

- No secrets in git. No `.env`, no keys. Commit `.env.example` instead.
- Label synthetic data as synthetic — in the code and in the report.
- Staging data only. Never production, never live M-Pesa.
- Tell Benjamin the same day if you find a real bug in the platform.
