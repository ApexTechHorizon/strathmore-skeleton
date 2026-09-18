# Master Prompt

Paste this at the start of a session with an AI coding assistant (Claude Code, Cursor, Copilot
Chat) so it has the context it needs and follows the rules we agreed. Fill in the bracketed
parts first.

Keep this file updated as the project changes. A stale master prompt produces confident wrong
answers.

---

## The prompt

```
You are helping me build [USE CASE TITLE], which is use case [U-CS __] on the
[Wasaa Lifestyle / Career Mentor OS] student programme.

## What the product is
[Two or three sentences. Copy from the Concept Note.]

## What I am building specifically
[One paragraph. The one organ of the system that is mine.]

## My service contract
Other teams call my service at this endpoint. It must not change without agreement.

  METHOD  /path
  in :  { ... }
  out:  { ... }

## Who I depend on
[Team number and what I need from them. "Nobody" if you are upstream.]

## Who depends on me
[Team numbers and what they take from me.]

## Stack
  Backend      : [e.g. Python 3.11, FastAPI]
  ML           : [e.g. scikit-learn, pandas]
  Web client   : [e.g. Next.js 15, TypeScript, Tailwind]
  Database     : [e.g. PostgreSQL 16, or "none, JSON files"]
  Hosting      : [e.g. Render]

## Rules for this project
1. Baseline before model. There is a simple version and a measured number for it.
   Do not suggest a complex model until the baseline exists and I know its score.
2. Never invent data. If something is synthetic, it must be labelled synthetic in
   the code and in the report.
3. Split by time, not at random, when holding out data. No leakage: never use a
   feature that would not be known at prediction time.
4. Money is decimal, never float.
5. No secrets in code. Environment variables only, with a .env.example committed.
6. Every response from our platform API is wrapped as { success, data, timestamp }.
   Unwrap it; never read response.data directly.
7. Small commits with conventional messages: feat:, fix:, docs:, test:, chore:
8. If you are not sure what I mean, ask me one question rather than guessing and
   writing 200 lines.

## How to answer me
- Show me the smallest change that works, then stop.
- Explain the reasoning in two or three sentences, not an essay.
- If you think my approach is wrong, say so plainly and say why.
- Tell me when something you suggest is a guess rather than something you checked.

## Right now I want to
[One specific thing. Not "build the project".]
```

---

## How to use it well

**Be specific about the ask.** "Build the matching system" produces something generic and
useless. "Write the function that filters mentors by budget, availability and language, before
any ranking" produces something you can actually use.

**Give it the real data shape.** Paste an actual sample record. It cannot guess your field names,
and it will invent plausible ones that do not exist.

**Do not accept the first answer if it does not make sense.** Ask why. If the reasoning is thin,
that is a signal — you are about to inherit code you cannot defend in a review.

**You are responsible for the code you submit.** "The AI wrote it" is not a defence when you are
asked how it works. If you cannot explain a line, do not commit it.

**Update this file as things change.** Especially the contract and the dependencies. Most bad
AI output comes from stale context, not a bad model.
