# Start Here

Every file in this folder, what it does, and the order to do it in.

---

## Every file, one line each

| File | What it does |
|---|---|
| `00-START-HERE.md` | This file. The index — what everything else is for |
| `MASTER_PROMPT.md` | The prompt you paste into an AI assistant so it knows your project and follows the rules |
| `GIT_AND_DEPLOYMENT.md` | Every git and Docker command you need, each with a one-line explanation |
| `PROJECT_Concept_Note.docx` | The shortest answer to "what is this and why does it matter" |
| `PROJECT_SRS.docx` | Every requirement, numbered, so you can later point at one and say whether it is done |
| `PROJECT_DDD.docx` | The shape of your data — what things exist, what they contain, how they relate |
| `PROJECT_TDD.docx` | How it is actually built — architecture, stack, your service contract, deployment |
| `PROJECT_Backend_Engineering_Document.docx` | The server: structure, endpoints, database, how to run it |
| `PROJECT_Frontend_Web_Engineering_Document.docx` | The user-facing web app: pages, state, API calls, styling |
| `PROJECT_Admin_Dashboard_Engineering_Document.docx` | The internal console: who can see what, and which decisions it supports |
| `PROJECT_Mobile_Flutter_Engineering_Document.docx` | The phone app: screens, state, offline behaviour, builds |
| `PROJECT_QA_and_Evaluation_Plan.docx` | How you prove it works — and how you prove the model beats the baseline |

---

## What the abbreviations mean

Nobody is born knowing these. Each document repeats its own definition on page one.

| Short | Stands for | In one line |
|---|---|---|
| **SRS** | Software Requirements Specification | Everything the system must do, each item numbered so it can be tested and ticked off |
| **DDD** | Detailed Design Document | The data — what things exist, what fields they hold, how they relate |
| **TDD** | Technical Design Document | How it is built: architecture, technology choices, interfaces, deployment |
| **QA** | Quality Assurance | What gets tested, how, and what counts as passing |

**Careful with TDD.** It also stands for *Test-Driven Development*, which is a way of writing
code, not a document. Here it always means the design document.

## The order to fill them in

| # | Document | When | Why it matters |
|---|---|---|---|
| 1 | Concept Note | Week 1 | If you cannot fill it in, you do not understand the problem yet |
| 2 | SRS | Week 1–2 | Numbered requirements, so "is it done" has an answer |
| 3 | DDD | Week 2 | The shape of your data. Expensive to fix later |
| 4 | TDD | Week 2–3 | How it is built, and your service contract |
| 5–8 | The four engineering documents | as you build | Only the ones you actually have |
| 9 | QA and Evaluation Plan | Week 3 onward | **The one marked hardest.** Baseline, metric, honest results |

**Delete what you do not need.** Most use cases are one service and a demo page. An empty
template in your hand-in is worse than no template.

Rename `PROJECT_` to your project name once you pick one.

---

## The two markdown files, in more detail

**`GIT_AND_DEPLOYMENT.md`** — read it before your first commit. Nine sections: starting a repo,
setting your git identity (do this first or your work is not credited to your GitHub account),
committing, connecting to GitHub, the daily loop, branches and pull requests, what never goes in
a repo, Docker, and free hosting.

**`MASTER_PROMPT.md`** — fill in the bracketed parts, then paste it at the start of a session
with Claude Code, Cursor or Copilot. It carries your context, your service contract, who you
depend on, and eight project rules. Keep it updated — most bad AI output comes from stale
context, not a bad model.

---

## Two things to get right early

**Your contract.** The endpoint other teams call — what goes in, what comes out. It is on your
card in the Team Integration Map. Copy it into the TDD and keep the two in step. If it has to
change, agree it with the teams on the other side first, then tell Benjamin so the map gets
reissued.

**Your baseline.** The dumbest version that works, and its number. Everything you build after is
judged against it. A clever model with no baseline cannot be marked.

---

## The order of work, for everything

```
baseline  ->  evaluation  ->  model  ->  integration
```

Build the simple version and measure it. Decide how you will know it worked. Then build the
clever thing. Then connect it.

Most teams want to start at the model. That is the mistake that costs the most marks.
