# Day 42 – Runners: GitHub-Hosted & Self-Hosted

## Overview

Today's tasks cover how GitHub Actions jobs get executed — using GitHub's managed runners across multiple OSes, and setting up a self-hosted runner on your own machine or VM.

---

## Task 1: GitHub-Hosted Runners — Three-Job Workflow

Three jobs run in parallel, each on a different OS. Each job prints the OS name, runner hostname, and current user.

**Screenshot of three-job workflow:**

![three-job workflow](screenshots/three-job.png)
https://github.com/Heyyprakhar1/github-actions-practice/

### What is a GitHub-hosted runner?

A GitHub-hosted runner is a virtual machine provisioned and managed entirely by GitHub. When a workflow triggers, GitHub spins up a fresh VM, runs your job, and tears it down when done. You don't configure, patch, or pay for the server directly — GitHub handles all of that. The runner is ephemeral: nothing persists between runs.

---

## Task 2: Pre-installed Software on ubuntu-latest

The ubuntu-latest job prints the versions of Docker, Python, Node, and Git — all pre-installed with zero setup.

**Why it matters:** Pre-installed tools mean you can start building, testing, and deploying immediately without spending steps installing common dependencies. It keeps workflows fast, clean, and focused on your actual logic rather than environment setup.

Full software manifest: [github.com/actions/runner-images](https://github.com/actions/runner-images)

---

## Task 3: Self-Hosted Runner Registration

Runner registered via **Settings → Actions → Runners → New self-hosted runner**, following the Linux setup instructions.

**Runner shows as Idle (green dot) in GitHub.**

Setup flow:
```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/...
tar xzf ./actions-runner-linux-x64.tar.gz
./config.sh --url https://github.com/<user>/<repo> --token <TOKEN>
./run.sh
```

To run as a persistent service:
```bash
sudo ./svc.sh install
sudo ./svc.sh start
```

---

## Task 4: Self-Hosted Workflow

**File:** `.github/workflows/self-hosted.yml`

The workflow prints the hostname (your own machine), working directory, creates `file1.txt`, and verifies it exists.

```yaml
name: self-hosted
on:
  push:
    branches: [main]

jobs:
  self-hosted:
    runs-on: [self-hosted, my-linux-runner]
    steps:
      - name: prints the hostname of the VM
        run: echo $HOSTNAME
      - name: prints the working directory
        run: pwd
      - name: creating a file
        run: touch file1.txt
      - name: verifying if the file exists
        run: cat file1.txt
```

**Verified:** `file1.txt` was created on the local machine after the run completed.

---

## Task 5: Labels

Label `my-linux-runner` was added to the self-hosted runner in GitHub settings. The workflow targets it with:

```yaml
runs-on: [self-hosted, my-linux-runner]
```

**Why labels matter:** When you have multiple self-hosted runners (e.g., one GPU machine, one ARM machine, one staging server), labels let you route specific jobs to the right hardware. Without labels, any available self-hosted runner picks up the job — labels give you precision.

---

## Task 6: GitHub-Hosted vs Self-Hosted

| | GitHub-Hosted | Self-Hosted |
|---|---|---|
| **Who manages it?** | GitHub (fully managed) | You (your machine or VM) |
| **Cost** | Included in free tier minutes; billed beyond that | Free to run; you pay for your own infrastructure |
| **Pre-installed tools** | Rich toolset (Docker, Python, Node, Git, etc.) | Only what you install yourself |
| **Good for** | Most CI/CD tasks, open source, standard builds | Specialized hardware, private networks, GPU jobs, cost optimization at scale |
| **Security concern** | Isolated ephemeral VM — safe for public repos | Persistent machine — untrusted PRs can run arbitrary code on your hardware |

---

## Key Takeaways

- GitHub-hosted runners are ephemeral, fully managed, and ideal for most workflows.
- Self-hosted runners give you full control over hardware, OS, and environment — critical for specialized or sensitive workloads.
- Labels are essential for directing jobs to the right runner when managing a fleet.
- Never use self-hosted runners on public repos without careful security controls — any fork can open a PR and trigger your runner.