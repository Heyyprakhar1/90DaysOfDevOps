# Day 43 — GitHub Actions: Jobs and Steps

Every workflow has three layers: the workflow, jobs inside it, and steps inside each job.
Steps are the smallest unit. They run sequentially inside their job — one finishes, the next starts.
```yaml
name: example-workflow

on:
  workflow_dispatch:

jobs:
  job-one:
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        run: echo "Hello from step 1"
      - name: Step 2
        run: echo "Hello from step 2"
```

Each job gets its own fresh runner. Nothing from one job leaks into another — not files, not env vars, nothing.

## Jobs Run in Parallel by Default

Two jobs with no dependency between them? GitHub spins up two runners at the same time.
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running lint"

  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running tests"
```

`lint` and `test` start simultaneously. That's the default and usually what you want.

## Controlling Order with `needs`

When a job actually depends on another finishing first, use `needs`.
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building project"

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - run: echo "Deploying project"
```

`deploy` waits for `build`. If `build` fails, `deploy` never runs. That second part matters — I've
seen people skip `needs` and watch a deploy kick off mid-build.

## Passing Data Between Jobs

Each job is isolated, so you can't just set a shell variable in job 1 and read it in job 2.
You need `outputs` — a formal handshake between jobs.
```yaml
jobs:
  generate-date:
    runs-on: ubuntu-latest

    outputs:
      today: ${{ steps.date.outputs.today }}

    steps:
      - id: date
        run: echo "today=$(date)" >> $GITHUB_OUTPUT

  print-date:
    runs-on: ubuntu-latest
    needs: generate-date

    steps:
      - run: echo "Today's date is ${{ needs.generate-date.outputs.today }}"
```

The step writes to `$GITHUB_OUTPUT`. The job exposes it under `outputs`. The downstream job reads it
via `needs.<job-name>.outputs.<key>`.

This pattern comes up more than you'd expect:
- Build job produces a Docker image tag → push job needs it
- Build captures a version string → deploy uses it to name the release
- Test job records a status → Slack notification job uses it to send the right message

The isolation-by-default thing trips people up at first. Once you accept that each job is a
completely fresh machine, `outputs` stops feeling like extra ceremony and just makes sense.

---

Repo: [github-actions-practice](https://github.com/Heyyprakhar1/github-actions-practice)