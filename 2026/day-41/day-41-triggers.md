# Day 41 – Triggers & Matrix Builds

## Objective

Understand different ways to trigger GitHub Actions workflows and learn how matrix builds allow CI pipelines to run across multiple environments simultaneously.

---

# Task 1 – Pull Request Trigger

### Goal

Create a workflow that runs automatically whenever a **Pull Request (PR)** is opened or updated against the `main` branch.

### Workflow File

```
.github/workflows/pr-check.yml
```

### Workflow Configuration

```yaml
name: PR Check

on:
  pull_request:
    branches: [main]

jobs:
  pr-check:
    runs-on: ubuntu-latest

    steps:
      - name: Print PR branch
        run: echo "PR check running for branch: ${{ github.head_ref }}"
```

### Steps Performed

1. Created a new workflow file inside `.github/workflows`.
2. Configured the workflow to trigger on **pull_request events**.
3. Created a new branch.
4. Pushed a commit.
5. Opened a **Pull Request against main**.

### Observation

The workflow automatically appeared under the **Checks section** in the Pull Request page and executed successfully.

---

# Task 2 – Scheduled Trigger

### Goal

Trigger a workflow automatically based on time using **cron syntax**.

### Workflow File

```
.github/workflows/schedule.yml
```

### Workflow Configuration

```yaml
name: Scheduled Workflow

on:
  schedule:
    - cron: "0 0 * * *"

jobs:
  scheduled-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print schedule message
        run: echo "This workflow runs every day at midnight UTC"
```

### Cron Expression Used

```
0 0 * * *
```

### Meaning

| Field   | Value |
| ------- | ----- |
| Minute  | 0     |
| Hour    | 0     |
| Day     | *     |
| Month   | *     |
| Weekday | *     |

This runs the workflow **every day at midnight (UTC)**.

### Additional Question

Cron expression for **every Monday at 9 AM**:

```
0 9 * * 1
```

---

# Task 3 – Manual Trigger

### Goal

Create a workflow that can be triggered manually from the **GitHub Actions UI**.

### Workflow File

```
.github/workflows/manual.yml
```

### Workflow Configuration

```yaml
name: Manual Workflow

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Select environment"
        required: true
        default: "staging"

jobs:
  manual-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print selected environment
        run: echo "Deploying to ${{ github.event.inputs.environment }}"
```

### Steps Performed

1. Added `workflow_dispatch` trigger.
2. Defined an **input parameter** named `environment`.
3. Triggered the workflow manually from:

```
GitHub → Actions → Run Workflow
```

### Observation

The workflow executed successfully and printed the selected environment value.

---

# Task 4 – Matrix Builds

### Goal

Run the same job across multiple environments using a **matrix strategy**.

### Workflow File

```
.github/workflows/matrix.yml
```

### Workflow Configuration

```yaml
name: Matrix Build Example

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        python-version: [3.11, 3.12, 3.13]
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Print Python Version
        run: python --version
```

### Matrix Configuration

Operating Systems:

* ubuntu-latest
* windows-latest
* macos-latest

Python Versions:

* 3.11
* 3.12
* 3.13

### Total Jobs Generated

```
3 OS × 3 Python versions = 9 jobs
```

### Observation

GitHub Actions automatically created **9 parallel jobs**, each running in a different environment.

---

# Task 5 – Exclude & Fail-Fast

### Goal

Modify the matrix to:

* Exclude a specific environment combination
* Control pipeline behavior when a job fails

### Updated Matrix Configuration

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: [3.11, 3.12, 3.13]
    os: [ubuntu-latest, windows-latest, macos-latest]

    exclude:
      - os: windows-latest
        python-version: 3.11
```

### Excluded Combination

```
Windows + Python 3.11
```

### Total Jobs After Exclusion

```
9 - 1 = 8 jobs
```

---

### Simulating a Failure

To observe fail-fast behavior, a job failure was intentionally triggered.

```yaml
- name: Simulate failure on Python 3.11
  if: matrix.python-version == '3.11'
  run: exit 1
```

---

### Fail-Fast Behavior

| Setting                   | Behavior                                              |
| ------------------------- | ----------------------------------------------------- |
| fail-fast: true (default) | Cancels remaining matrix jobs after first failure     |
| fail-fast: false          | Allows all jobs to continue running even if one fails |

### Observation

With `fail-fast: false`, even though Python 3.11 jobs failed, the remaining jobs continued running.

---

# Key Learnings

* GitHub Actions workflows can be triggered in multiple ways:

  * Push events
  * Pull Requests
  * Scheduled cron jobs
  * Manual triggers

* **Matrix builds** allow CI pipelines to test across multiple environments automatically.

* **Exclude** removes specific environment combinations from a matrix.

* **Fail-fast** controls whether remaining jobs stop after a failure.

---

# Conclusion

Day-41 introduced advanced workflow triggering mechanisms and matrix builds in GitHub Actions. These concepts are widely used in real CI/CD pipelines to ensure applications are tested across different environments efficiently while controlling pipeline execution behavior.