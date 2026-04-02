---
name: git-branch-manager
description: "Manage, audit, and clean up Git branches efficiently. Use when listing branches, finding stale branches, checking branch age/activity, identifying merged branches for deletion, comparing branches, or doing bulk branch operations. Triggers on: clean up branches, delete merged branches, find stale branches, branch age, which branches are old, compare branches, list all branches sorted by date, branch activity, git branch audit."
---

# Git Branch Manager

Manage, audit, and clean up Git branches with confidence.

## Core Commands Reference

### List Branches

```bash
# Local branches with last commit date, sorted by most recent
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/

# Remote branches
git branch -r

# All branches (local + remote)
git branch -a

# Branches with tracking info
git branch -vv

# Only merged branches (safe to delete after confirming)
git branch --merged

# Only unmerged branches
git branch --no-merged
```

### Find Stale Branches

```bash
# Branches not touched in N days (e.g., 30 days)
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(committerdate:relative)' refs/heads/ | awk '$1 <= $(date -d "30 days ago" +%Y-%m-%d)'

# PowerShell version
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/ | Where-Object { $_.Split(' ')[0] -le (Get-Date).AddDays(-30).ToString('yyyy-MM-dd') }
```

### Check Branch Activity

```bash
# Show commits on branch not in main/master
git log main..HEAD --oneline

# Count commits ahead/behind
git rev-list --left-right --count main...HEAD

# Last commit author and time for each branch
git for-each-ref --sort=-committerdate --format='%(committerdate:relative) %(authorname) %(refname:short)' refs/heads/
```

### Delete Merged Branches Safely

```bash
# 1. Identify merged branches (won't delete main/master/develop)
git branch --merged main

# 2. Dry run - show what would be deleted
git branch --merged main | grep -v -E '(\*|main|master|develop)' | xargs -n 1 echo "Would delete:"

# 3. Actually delete (after confirmation)
git branch --merged main | grep -v -E '(\*|main|master|develop)' | xargs git branch -d

# Force delete unmerged branches (use with caution)
git branch -D <branch-name>
```

### Bulk Operations

```bash
# Delete multiple branches at once
git branch -D branch1 branch2 branch3

# Delete by pattern
git branch | grep 'pattern' | xargs git branch -d

# Rename current branch
git branch -m <new-name>

# Set upstream to track remote
git branch -u origin/feature-branch
```

### Remote Operations

```bash
# Push and set upstream in one command
git push -u origin feature-branch

# Delete remote branch
git push origin --delete remote-branch

# Prune stale remote tracking branches
git fetch --prune

# Or set auto-prune globally
git config --global fetch.prune true
```

## Branch Cleanup Workflow

### Step 1: Audit

```
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(committerdate:relative)' refs/heads/
```

Identify:
- Which branches are very old (>90 days)
- Which are already merged
- Which are actively being worked on

### Step 2: Categorize

| Category | Action |
|---|---|
| Merged into main, old | Delete |
| Unmerged, old (>90 days, no commits) | Investigate, likely delete |
| Unmerged, recent commits | Keep or discuss with author |
| Feature complete, waiting review | Keep |
| Main/master/develop | Never delete |

### Step 3: Confirm Before Bulk Delete

Always dry-run first. For unmerged branches, check with team or warn before force-deleting.

### Step 4: Execute

Delete in batches. Don't delete everything at once — you can't undo a `git branch -D`.

## Common Scenarios

### "My repo has 50+ branches, where do I start?"

```bash
# Find the 10 most recently active branches
git for-each-ref --sort=-committerdate --count=10 --format='%(committerdate:short) %(refname:short)' refs/heads/

# Find branches with no recent commits (>60 days)
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/ | awk '$1 <= "'$(date -d "60 days ago" +%Y-%m-%d)'"'
```

### "Which branches are ahead of main?"

```bash
git branch -r --format='%(refname:short) %(upstream:track)' | grep -v '\[gone\]'
```

### "I accidentally merged a branch I shouldn't have"

```bash
# Find the merge commit
git log --oneline --grep="Merge branch" | head -20

# Revert the merge (creates new commit undoing the merge)
git revert -m 1 <merge-commit-sha>

# Or reset (if merge was recent and you haven't pushed)
git reset --hard main
```

## Reference Files

- `references/common-patterns.md` — Ready-to-use one-liners for common tasks
- `references/safety-checklist.md` — Pre-delete safety checklist
