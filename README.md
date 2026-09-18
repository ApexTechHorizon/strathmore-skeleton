# Strathmore Use-Case Skeleton

Starting point for the Strathmore use-case projects on **Wasaa Lifestyle** and
**Career Mentor OS**.

---

## Students: start here

**Find your folder in `starters/`.** It is already filled in with your contract — your
endpoint, what goes in, what comes out, who you depend on, and who depends on you.

| | |
|---|---|
| `starters/<your-name>/` | **Your project.** Copy this out and make it your own repo |
| `documents/` | Templates for the write-up. Copy in the ones you need |
| `platform/` | Benjamin's integration layer. **You can ignore this** |

### Getting your own copy

```bash
git clone --depth 1 https://github.com/ApexTechHorizon/strathmore-skeleton.git
cp -r strathmore-skeleton/starters/<your-name> ~/my-project
cp -r strathmore-skeleton/documents ~/my-project/documents
cd ~/my-project && git init -b main
```

Then create an empty repo on GitHub **under your own account**, named after your use case,
and push to it. Add Benjamin as a collaborator and send him the link.

### Run it

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open <http://localhost:8000/docs> for interactive API docs, or `demo/index.html` for the
mini app. `pytest -q` runs the contract test.

---

## The 18 starters

### Wasaa Lifestyle — Friday 2 October

| Folder | Use case | What your service does |
|---|---|---|
| `budget-forecast` | U-CS 37 | What a household will spend next month, per category |
| `spend-advisor` | U-CS 38 | Three things they could do differently, with shilling figures |
| `marketplace-search` | U-CS 39 | Better search results, and spotting manipulated reviews |
| `provider-match` | U-CS 40 | Rank providers most likely to finish the job well |
| `scheduling` | U-CS 41 | Correct slots, and predicting no-shows |
| `wallet-checks` | U-CS 42 | Prove the money is always correct |
| `dependant-costs` | U-CS 43 | What supporting a child costs over 1, 5 and 10 years |
| `access-pass` | U-CS 44 | A gate pass that works offline and cannot be shared |
| `emergency-triage` | U-CS 45 | Route it, escalate it, never lose it quietly |
| `ops-metrics` | U-CS 46 | Six numbers that drive a decision this week |

### Career Mentor OS — Friday 16 October

| Folder | Use case | What your service does |
|---|---|---|
| `skills-gap` | U-CS 3 | What can they do, what are they missing. **Two teams wait on you** |
| `career-path` | U-CS 1 | The realistic next role |
| `matching` | U-CS 2 | Which mentor, within budget and availability |
| `chatbot` | U-CS 4 | Answers the easy questions, hands over when hard |
| `session-value` | U-CS 5 | Will this session help, predicted beforehand |
| `pricing` | U-CS 6 | A price both sides say yes to |
| `analytics` | U-CS 7 | What a cohort did and whether it mattered |
| `micro-learning` | U-CS 8 | The next lesson that closes a real gap |

---

## The order of work

```
baseline  ->  evaluation  ->  model  ->  integration
```

1. **Baseline.** The dumbest thing that works. Measure it. **Write the number down.**
2. **Evaluation.** Pick your metric. Split by time, not at random. Hold the last part back.
3. **Model.** Build the real thing. Show it beats the baseline.
4. **Integration.** Keep the contract identical while the inside changes. Deploy. Send the URL.

Most teams want to start at the model. That is the mistake that costs the most marks.

## What you hand in

- A GitHub repo, with Benjamin added as a collaborator
- A live URL that answers
- The filled-in documents
- A README a stranger could run it from

## Rules

- **No secrets in git.** No `.env`, no keys, no keystores. Commit `.env.example` instead.
- **Label synthetic data as synthetic** — in the code and in the report.
- **Staging only.** No production data, no live M-Pesa.
- **Money is decimal, never float.**
- Tell Benjamin the same day if you find a real bug in the platform.

---

## For the engineer-in-charge

`platform/` holds the integration layer. `platform/backend/src/modules/` has one adapter per
team: set `<NAME>_SERVICE_URL` in `.env` and it calls their hosted service. Until a URL is set
the adapter returns a clean `503`, so one late team never takes the platform down.
`GET /<module>/status` reports whether a service is configured and up.
