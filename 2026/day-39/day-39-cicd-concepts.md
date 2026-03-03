# Day 39 – What is CI/CD?

---

## Task 1: The Problem

### What can go wrong with 5 devs manually deploying?
- Two developers push conflicting code at the same time — one overwrites the other's changes (merge conflicts)
- A dev deploys untested code directly to production, breaking the live app
- No one knows who deployed what or when — debugging becomes a blame game
- One dev's environment has a different Python/Node version — works locally, crashes in prod
- No rollback plan — if the deploy breaks things, the team scrambles manually to fix it

### "It works on my machine" — why it's a real problem
This happens when a developer's local environment differs from the server:
different OS, different dependency versions, different env variables, different config files.
CI/CD solves this by running code in a **clean, controlled, identical environment every time** —
no "my machine" bias.

### How many times can a team safely deploy manually?
Realistically: **1–2 times a day**, if they're disciplined.
With CI/CD and automation: teams like Netflix and Amazon deploy **hundreds of times per day**.
Manual deploys don't scale — CI/CD does.

---

## Task 2: CI vs CD vs CD

### Continuous Integration (CI)
Developers merge code to a shared branch frequently (multiple times a day).
Every merge automatically triggers tests and builds.
It catches bugs early — before they pile up into a broken mess.

**Real-world example:** A developer opens a Pull Request on GitHub.
GitHub Actions immediately runs unit tests. If tests fail, the PR is blocked from merging.

---

### Continuous Delivery (CD)
Everything CI does, plus: the code is automatically prepared and ready to deploy to production
at any time — but a **human still clicks the deploy button**.
"Delivery" means the software is always in a deployable state.

**Real-world example:** After tests pass, the pipeline builds a Docker image and pushes it
to a staging environment. The team reviews it, then manually triggers the production deploy.

---

### Continuous Deployment (CD)
Goes one step further than Delivery — **no human approval needed**.
Every change that passes all tests is automatically deployed straight to production.
Used by teams with high test confidence and mature pipelines.

**Real-world example:** A dev merges to `main` on Friday afternoon.
Within 10 minutes, the change is live on production with zero manual steps.
Teams like Etsy and Flickr use this model.

---

## Task 3: Pipeline Anatomy

| Term | What it does |
|------|-------------|
| **Trigger** | The event that starts the pipeline — e.g. a `git push`, a PR, or a scheduled cron job |
| **Stage** | A logical phase of the pipeline — e.g. `build`, `test`, `deploy`. Stages run in order |
| **Job** | A unit of work inside a stage — e.g. "run unit tests" or "build Docker image" |
| **Step** | A single command or action inside a job — e.g. `run: pytest tests/` |
| **Runner** | The machine (VM or container) that actually executes the job — GitHub-hosted or self-hosted |
| **Artifact** | Output produced by a job that can be passed to the next stage — e.g. a compiled binary, Docker image, coverage report |

---

## Task 4: Pipeline Diagram

```
Developer pushes code to GitHub
            │
            ▼
    ┌───────────────┐
    │   TRIGGER     │  on: push to main / pull_request
    └──────┬────────┘
           │
           ▼
    ┌───────────────────────────────────────┐
    │           STAGE 1: TEST               │
    │  - Checkout code                      │
    │  - Install dependencies               │
    │  - Run unit tests (pytest / jest)     │
    │  - Lint check                         │
    │  ✅ Pass → continue  ❌ Fail → stop  │
    └──────────────┬────────────────────────┘
                   │
                   ▼
    ┌───────────────────────────────────────┐
    │           STAGE 2: BUILD              │
    │  - Build Docker image                 │
    │  - Tag image with git SHA             │
    │  - Push image to Docker Hub / ECR     │
    │  📦 Artifact: Docker image            │
    └──────────────┬────────────────────────┘
                   │
                   ▼
    ┌───────────────────────────────────────┐
    │        STAGE 3: DEPLOY                │
    │  - Pull Docker image on staging       │
    │  - Run docker-compose up              │
    │  - Health check endpoint              │
    │  🚀 App live on staging server       │
    └───────────────────────────────────────┘
```

---

## Task 5: Real-World Pipeline — FastAPI on GitHub

**Repo:** `fastapi/fastapi`
**File:** `.github/workflows/test.yml`

### What triggers it?
Three triggers:
- `push` to the `master` branch
- `pull_request` when opened or updated (`synchronize`)
- `schedule` — runs automatically every Monday at midnight (cron: `0 0 * * 1`)

### How many jobs does it have?
**3 jobs:**
1. `test` — runs the actual test suite
2. `coverage-combine` — merges coverage reports from all matrix runs
3. `check` — a final gate job used for branch protection rules (does nothing except confirm all others passed)

### What does it do?
The `test` job uses a **matrix strategy** — it runs tests in parallel across multiple
OS and Python version combinations (Ubuntu, macOS, Windows × Python 3.9 through 3.14).
It installs dependencies via `uv`, runs the test suite, and uploads coverage files as artifacts.
The `coverage-combine` job then downloads all those coverage files, merges them,
generates an HTML coverage report, and enforces **100% code coverage** — if coverage drops
below 100%, the pipeline fails.

---

## 3 Key Learnings

1. **CI/CD is a practice, not a tool.** GitHub Actions, Jenkins, GitLab CI are just tools
   that implement the practice. The principle is: automate everything that can be automated
   between writing code and shipping it.

2. **A failing pipeline is a good thing.** It means CI/CD caught a bug before it hit production.
   The goal is to fail fast and fix fast — not to have green pipelines by skipping tests.

3. **Continuous Deployment requires trust in your tests.** You can only auto-deploy to production
   if your test suite is comprehensive enough to catch regressions. FastAPI enforcing 100% coverage
   is a great example of building that trust.