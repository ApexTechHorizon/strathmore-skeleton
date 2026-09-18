# Git, Docker and Deployment

Short explanations, then the exact commands. Copy and paste them.

**The rule: every subfolder is its own repository.** `backend`, `web-client`, `web-admin`,
`flutter` and `ml-service` each get their own GitHub repo. They are separate things that get
deployed separately, so they version separately. `documents` can live in whichever repo you
prefer, or its own.

---

## 1. Starting a repo

`git init` turns a plain folder into a repository — it starts tracking changes. You do this
once per folder.

```bash
cd backend
git init -b main
```

`-b main` names your first branch `main` instead of `master`.

### Tell git who you are

Do this **before your first commit**, or your work will not be credited to your GitHub account.

```bash
git config user.name  "Your Name"
git config user.email "the-email-on-your-github-account@example.com"
```

Without the `--global` flag this applies to this repo only, which is what you want.

---

## 2. Your first commit

A **commit** is a saved snapshot with a message explaining what changed.

```bash
git add .                          # stage everything (respects .gitignore)
git commit -m "chore: initial project skeleton"
```

`git add .` picks what goes in the snapshot. `git commit` saves it.

### Check before you commit

```bash
git status                         # what has changed
git diff                           # exactly what changed, line by line
```

Get into the habit of running `git status` before every commit. It is how you avoid committing
a 200MB model file or a `.env` full of secrets.

---

## 3. Connecting to GitHub

Create an **empty** repo on GitHub first — no README, no .gitignore, or you will get a conflict.

```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

A **remote** is a copy of your repo that lives somewhere else. `origin` is just the conventional
name for the main one. `-u` links your local `main` to the remote `main`, so afterwards you can
type plain `git push`.

---

## 4. The daily loop

```bash
git status                         # see what changed
git add .                          # stage it
git commit -m "feat: add skills gap endpoint"
git push                           # send it to GitHub
```

Commit often — several times a day, not once a week. Small commits are easy to undo. A single
enormous commit at the end is worth nothing to anybody reviewing your work.

### Commit message style

```
feat:     a new feature
fix:      a bug fix
docs:     documentation only
refactor: restructuring, no behaviour change
test:     adding or fixing tests
chore:    tooling, config, dependencies
```

Write what changed, not what you did. `fix: reject bookings with no available slot` beats
`fixed stuff`.

---

## 5. Branches

A **branch** is a parallel line of work, so you can build something risky without breaking
`main`.

```bash
git checkout -b feat/mentor-matching     # create and switch to a branch
# ... work, add, commit ...
git push -u origin feat/mentor-matching  # push the branch
```

Then open a **Pull Request** on GitHub to merge it into `main`. Get a teammate to look at it
first. That review is often where the real learning happens.

### Getting other people's work

```bash
git pull                           # fetch and merge the latest main
```

Pull before you start work each day. It is much easier than untangling a conflict later.

---

## 6. What never goes in a repo

Put these in `.gitignore` before your first commit:

```
.env
.env.local
node_modules/
__pycache__/
venv/
*.pyc
build/
dist/
.DS_Store
*.keystore
*.jks
*.p12
model.pkl          # large model files — use releases or cloud storage
data/*.csv         # large datasets
```

**Never commit:** passwords, API keys, tokens, `.env` files, signing keystores, or anything
over about 50MB. A secret pushed to GitHub is public the moment it lands, even if you delete it
afterwards — the history keeps it. If it happens, rotate the key immediately and tell me.

Commit a `.env.example` instead — same variable names, fake values — so the next person knows
what to fill in.

---

## 7. Docker

Docker packages your app with everything it needs to run, so it behaves the same on your laptop,
your teammate's laptop and the server. This is why every folder here has a `Dockerfile`.

```bash
docker build -t my-service .              # build an image from the Dockerfile
docker run -p 8000:8000 --env-file .env my-service
```

`-p 8000:8000` maps a port on your machine to a port inside the container. `--env-file` passes
in your environment variables without baking them into the image.

To run several services together, use `docker compose`:

```bash
docker compose up --build       # start everything
docker compose down             # stop everything
```

### Check it works before you deploy

```bash
docker build -t my-service . && docker run -p 8000:8000 my-service
curl http://localhost:8000/health
```

If that returns something sensible, hosting will almost certainly work.

---

## 8. Hosting it free

You need a public URL. Any of these are free enough for this project:

| Service | Good for | Notes |
|---|---|---|
| **Render** | Docker services, APIs | Easiest. Connect the GitHub repo, it finds the Dockerfile |
| **Railway** | Docker, databases | Generous free tier, Postgres included |
| **Fly.io** | Docker, close to users | `fly launch` reads your Dockerfile |
| **Hugging Face Spaces** | ML services and demos | Best for a Python model with a simple UI |
| **Vercel** | Next.js web clients | Made for it, near-zero config |

The usual flow: push to GitHub, connect the repo on the host, set environment variables in their
dashboard, deploy. Most of them redeploy automatically on every push to `main`.

**Free tiers sleep.** A service with no traffic may take 30 seconds to wake. Mention that when
you demo, or hit the URL a minute beforehand.

---

## 9. What you hand in

- A GitHub repo URL for each folder you used
- A live URL for your service
- A `README.md` at the root of each repo that explains how to run it
- Your documents folder, filled in

The README is the first thing anybody opens. If somebody cannot run your project from it, it is
not finished.

---

## Quick reference

```bash
git init -b main                              # start a repo
git config user.name "..."                    # identify yourself
git config user.email "..."
git status                                    # what changed
git add .                                     # stage everything
git commit -m "feat: ..."                     # save a snapshot
git remote add origin <url>                   # connect to GitHub
git push -u origin main                       # first push
git push                                      # every push after
git pull                                      # get teammates' work
git checkout -b feat/thing                    # new branch
git log --oneline -10                         # recent history

docker build -t name .                        # build image
docker run -p 8000:8000 name                  # run it
docker compose up --build                     # run everything
```
