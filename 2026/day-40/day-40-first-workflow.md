# Day 40 – My First GitHub Actions Workflow

**Repository:** [github-actions-practice](https://github.com/Heyyprakhar1/github-actions-practice)  
**Challenge:** #90DaysOfDevOps – Day 40  
**Topic:** Introduction to GitHub Actions & CI/CD

---

## 📁 Deliverables

| File | Description |
|------|-------------|
| `.github/workflows/hello.yml` | The workflow file that runs on every push |
| `day-40-first-workflow.md` | This documentation file |

---

## ✅ Task 1 – Repository Setup

1. Created a new **public** GitHub repository called `github-actions-practice`
2. Cloned it locally:
   ```bash
   git clone https://github.com/Heyyprakhar1/github-actions-practice.git
   cd github-actions-practice
   ```
3. Created the required folder structure:
   ```bash
   mkdir -p .github/workflows
   ```

---

## ✅ Task 2 – Hello Workflow

### Workflow File: `.github/workflows/hello.yml`


After pushing this file, I navigated to the **Actions** tab on GitHub and watched the workflow run in real-time. The pipeline turned **green ✅** on first success.

---

## ✅ Task 3 – Anatomy of the Workflow File

Here's what each key in the workflow YAML does, in my own words:

| Key | What it does |
|-----|-------------|
| `on:` | Defines the **trigger** — when should this workflow run? In our case, it runs on every `push` to the `main` branch. |
| `jobs:` | A workflow is made up of one or more **jobs**. Each job is a separate unit of work that runs independently (unless you set dependencies). |
| `runs-on:` | Specifies the **type of virtual machine** (runner) that the job should execute on. `ubuntu-latest` means a fresh Ubuntu Linux environment hosted by GitHub. |
| `steps:` | The **ordered list of tasks** within a job. Each step either runs a shell command or uses a pre-built action. |
| `uses:` | Tells GitHub Actions to use a **pre-built, reusable action** from the Marketplace. For example, `actions/checkout@v4` clones your repository onto the runner. |
| `run:` | Executes a **shell command** directly on the runner. Think of it like typing a command in your terminal. |
| `name:` (on a step) | A **human-readable label** for the step. This name appears in the Actions UI, making it easy to identify which step is running or failed. |

---

## ✅ Task 4 – Extended Steps

The final `hello.yml` was updated to include four additional steps:

1. **Print current date and time** – `run: date`
2. **Print branch name** – using the built-in GitHub context variable `${{ github.ref_name }}`
3. **List files in the repo** – `run: ls -la`
4. **Print runner OS** – using the environment variable `$RUNNER_OS`

Each push triggered a new workflow run, visible in the **Actions** tab with all steps shown.

---

## ✅ Task 5 – Breaking It On Purpose

### What I did:

Added a step that intentionally fails:

```yaml
- name: This will fail
  run: exit 1
```

### What happened:

- The pipeline turned **red ❌** in the Actions tab
- The failing step was highlighted in red inside the job view
- All steps *after* the failing step were **skipped** automatically
- GitHub showed a clear error: `Process completed with exit code 1`

### How to read a failed pipeline:

1. Go to the **Actions** tab in your repo
2. Click on the **failed run** (shown with a red ✗ icon)
3. Click on the **job name** (e.g., `greet`)
4. Expand the **failed step** — it will show the exact command output and error message
5. Fix the issue, push again, and a new run will start

### After the fix:

Removed the `exit 1` step and pushed again. The pipeline went back to **green ✅**.

---

## 🖼️ Screenshot – Green Pipeline Run

> **Note:** Replace the placeholder below with an actual screenshot from your GitHub Actions tab.

```
[ Screenshot: Actions tab showing a green ✅ workflow run ]
[ Job: greet — all steps passed ]
```

*To take a screenshot: Go to your repo → Actions tab → click the latest run → capture the page showing all green checkmarks.*

---

## 💡 Key Takeaways

- **GitHub Actions** is a CI/CD platform built directly into GitHub — no external tools needed to get started.
- Workflows are defined as **YAML files** inside `.github/workflows/`.
- Every `push` can automatically trigger builds, tests, or deployments.
- The **Actions tab** gives full visibility into every run — what passed, what failed, and the complete logs.
- Built-in **context variables** like `${{ github.ref_name }}` and `${{ github.actor }}` make workflows dynamic without extra configuration.
- A failed step **stops the job** by default and turns the pipeline red — making it easy to catch issues early.

---