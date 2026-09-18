# chatbot  —  U-CS 4

**AI Career Coaching Chatbot** · Career Mentor OS

Answer the easy questions from real content, with sources, and hand over when it gets hard.

---

## Your contract

This is the shape the rest of the system expects. Agree any change with the teams below,
then tell Benjamin so the Team Integration Map gets reissued.

```
POST /ask
  in : { "question": "...", "userId": "..." }
  out: { "answer": "...", "citations": [], "handover": false, "handoverReason": null }
```

**Call it `chatbot` everywhere** — your repo name, your service URL, your route, and the
variable Benjamin sets when integrating you: `CHATBOT_SERVICE_URL`

## Who you depend on

U-CS 8 (micro-learning) for the content to answer from.

## Who depends on you

Nobody directly — but you are what makes mentor time go further.

## Done when

Write 50 questions and good answers BEFORE building. Every answer cites a source. It hands over quickly.

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
docker build -t chatbot . && docker run -p 8000:8000 chatbot
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
