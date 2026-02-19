# Day 23 – Git Branching & Working with GitHub (Notes)

## Task 1️⃣ Understanding Branches

### 1. What is a branch in Git?

A branch is a movable pointer to a specific commit. It allows you to develop features or fixes independently without affecting other parts of the project.

### 2. Why use branches instead of committing everything to `main`?

Branches isolate work. This prevents unstable or incomplete code from affecting the main production-ready branch.

### 3. What is `HEAD` in Git?

`HEAD` is a pointer to the current active branch and the latest commit on that branch. It tells Git where you are in the commit history.

### 4. What happens to files when switching branches?

Git updates your working directory to match the snapshot of the branch you switch to. Files may change, appear, or disappear depending on that branch’s state.

---

## Task 2️⃣ Branching Concepts

* `git branch` → Lists all local branches.
* `git branch <name>` → Creates a new branch.
* `git switch <name>` → Switches to a branch (modern command).
* `git checkout <name>` → Older command used for switching branches and restoring files.
* `git switch -c <name>` → Create and switch in one command.
* `git branch -d <name>` → Delete a branch safely.

### Difference: `git switch` vs `git checkout`

* `git switch` is focused only on branch switching.
* `git checkout` is multifunctional (switch branches + restore files), which can be confusing.

---

## Task 3️⃣ Working with GitHub (Push Concepts)

### What is `origin`?

`origin` is the default name given to the remote repository you cloned from or connected to.

### What is `upstream`?

`upstream` refers to the original repository from which a fork was created. It is used to sync changes from the main source project.

### Local vs Remote Branch

* Local branch exists on your machine.
* Remote branch exists on GitHub (or another remote server).

---

## Task 4️⃣ Fetch vs Pull

### `git fetch`

Downloads changes from remote but does not merge them automatically.

### `git pull`

Fetches changes and immediately merges them into the current branch.

Pull = Fetch + Merge.

---

## Task 5️⃣ Clone vs Fork

### Clone

Creates a local copy of an existing repository on your machine.
Used when you have direct access or only need a local copy.

### Fork

Creates a copy of someone else's repository under your GitHub account.
Used when contributing to open-source or when you don't have direct write access.

### When to Clone vs Fork

* Clone → Personal projects or team repos with access.
* Fork → Contributing to external/open-source projects.

### Keeping Fork in Sync

1. Add original repo as `upstream` remote.
2. Run `git fetch upstream`.
3. Merge or rebase from `upstream/main`.

---

## Summary Understanding

* Branching enables safe parallel development.
* `main` should stay stable and production-ready.
* Remote repositories enable collaboration.
* Forking is a GitHub workflow concept built on top of Git.
* Clean branching strategy is essential in DevOps pipelines.

