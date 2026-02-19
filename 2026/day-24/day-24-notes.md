# Day 24 – Advanced Git: Merge, Rebase, Stash & Cherry Pick

Welcome to Day 24 of #90DaysOfDevOps 🚀  
Today focuses on advanced Git operations that are essential for real-world collaboration and clean version control workflows.

This is where Git starts to feel powerful.

---

## 📌 Objectives

By the end of this day, you should understand:

- How branches are merged back together
- The difference between **merge** and **rebase**
- When to use **squash merge**
- How to temporarily save work using **git stash**
- How to selectively apply commits using **cherry-pick**

---

# 🔀 1. Git Merge

## What is Merge?

`git merge` combines changes from one branch into another.

### Types of Merge

### ✅ Fast-Forward Merge
- Happens when no new commits exist on the target branch.
- Git simply moves the branch pointer forward.
- Clean and linear history.

### ✅ Merge Commit
- Happens when both branches have new commits.
- Git creates a special merge commit.
- History becomes non-linear.

### ⚠️ Merge Conflict
Occurs when:
- The same file
- The same line
- Is modified differently in two branches.

Git pauses and asks you to resolve it manually.

---

# 🔁 2. Git Rebase

## What is Rebase?

Rebase rewrites commit history by moving your branch commits on top of another branch.

Instead of combining histories like merge, it *replays* commits.

### 🔍 What Rebase Does:
- Takes your feature branch commits
- Reapplies them on top of the latest `main`
- Creates a clean, linear history

### 🚫 Important Rule:
Never rebase commits that are already pushed and shared with others.

Rebase rewrites history. That can break collaboration.

---

## Merge vs Rebase

| Feature | Merge | Rebase |
|----------|--------|---------|
| History | Preserves history | Rewrites history |
| Commit Graph | Non-linear | Linear |
| Safe for Shared Branch? | Yes | No |
| Clean History? | Sometimes | Yes |

---

# 🧱 3. Squash Merge

## What is Squash?

Squash merge combines multiple commits into a single commit before merging.

Instead of adding 5 small commits, you get 1 clean commit.

### When to Use Squash?
- Small fixes
- Typo commits
- Formatting changes
- Keeping `main` clean

### Trade-off:
You lose detailed commit history from the feature branch.

---

# 🧳 4. Git Stash

## What is Stash?

`git stash` temporarily saves uncommitted changes so you can switch branches.

Useful when:
- You’re mid-work
- An urgent task comes up
- You don’t want to commit unfinished code

### Common Commands

- `git stash`
- `git stash list`
- `git stash pop`
- `git stash apply`

### Difference:
- `pop` → applies and removes stash
- `apply` → applies but keeps stash

---

# 🍒 5. Cherry Pick

## What is Cherry Pick?

`git cherry-pick <commit-hash>`

Applies a specific commit from one branch onto another.

### When to Use:
- Hotfix from production branch
- Applying a single useful commit
- Backporting fixes

### Risks:
- Duplicate commits
- Conflicts
- Confusing history if overused

---

# 🧠 Key Takeaways

- Merge preserves history.
- Rebase rewrites history.
- Squash keeps main clean.
- Stash helps during context switching.
- Cherry-pick is surgical commit transfer.

Advanced Git is about:
✔ Clean history  
✔ Safe collaboration  
✔ Intentional workflow  

---

# 📊 Helpful Command for Visualization

```bash
git log --oneline --graph --all

