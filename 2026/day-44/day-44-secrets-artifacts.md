# Day 44 – GitHub Secrets, artefacts, and CI Tests

## Overview

Today’s tasks focused on learning how **GitHub Actions handles secrets, artefacts, and CI test execution**.
The goal was to securely manage sensitive information, transfer files between workflow jobs, and run automated tests inside a CI pipeline.

---

# Task 1 – GitHub Secrets

## Secret Created

Repository → **Settings → Secrets and Variables → Actions**

Secret name:

```
MY_SECRET_MESSAGE
```

### Workflow Behavior

The workflow checked whether the secret exists and printed:

```
The secret is set: true
```

### Attempt to Print Secret

When attempting to print:

```
${{ secrets.MY_SECRET_MESSAGE }}
```

GitHub automatically **masks the value in logs**.

Example output:

```
***
```

### Why Secrets Should Never Be Printed

Secrets must never be printed in CI logs because:

* CI logs are visible to repository collaborators
* Logs may be stored for a long time
* Exposed credentials could allow unauthorized access
* Attackers could misuse API keys, tokens, or passwords

GitHub automatically masks secrets to prevent accidental exposure.

---

# Task 2 – Using Secrets as Environment Variables

Secrets were passed as environment variables inside a workflow step.

Example:

```yaml
env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_TOKEN: ${{ secrets.DOCKER_TOKEN }}
```

These values can be used safely in commands without hardcoding them into the repository.

Example command:

```bash
echo "Docker login using secrets"
```

This ensures **secure authentication for Docker Hub in future CI pipelines**.

---

# Task 3 – Upload artefacts

A workflow step generated a file:

```
test-report.txt
```

Example content:

```
CI test executed successfully
```

artefact upload step:

```yaml
- uses: actions/upload-artefact@v4
  with:
    name: test-report
    path: test-report.txt
```

After the workflow completed, the artefact appeared in the **Actions tab** where it could be downloaded.

### Screenshot

(Add screenshot of artefact download here)

---

# Task 4 – Download artefacts Between Jobs

Artefacts allow files to be shared between different jobs in a workflow.

### Job 1

* Generates a file
* Uploads it as an artefact

### Job 2

* Downloads the artefact
* Prints its contents

Example use case in real pipelines:

* Sharing build outputs between jobs
* Passing compiled binaries to deployment steps
* Storing test reports or logs

---

# Task 5 – Running Real Tests in CI

A script from the repository was executed inside the CI pipeline.

Pipeline steps:

1. Checkout repository code
2. Install dependencies
3. Run the test script

Example command:

```bash
python scripts/test_script.py
```

### Pipeline Failure Test

The script was intentionally broken to confirm CI behavior.

Result:

* Pipeline turned **red (failed)**

After fixing the script:

* Pipeline turned **green (success)**

This confirms CI correctly detects failures.

### Screenshot

(Add screenshot of successful CI run here)

---

# Task 6 – Caching Dependencies

Caching was added to speed up dependency installation.

Example cache configuration:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### What Is Cached

Downloaded Python packages from pip.

### Where Is It Stored

GitHub stores the cache in its **internal cloud storage**, associated with the repository and cache key.

### Benefit

Subsequent workflow runs restore dependencies from cache instead of downloading them again, significantly reducing CI execution time.

---

# Key Learnings

* GitHub Secrets securely store sensitive data for workflows
* Secrets should never be printed in logs
* Artefacts allow files to be transferred between jobs
* CI pipelines automatically fail if a script exits with a non-zero status code
* Dependency caching improves pipeline performance and reduces build time

---

# Outcome

✔ Implemented secrets management
✔ Uploaded and downloaded artefacts
✔ Executed real tests in CI
✔ Implemented dependency caching
✔ Verified successful pipeline execution
