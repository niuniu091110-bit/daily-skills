# Branch Deletion Safety Checklist

## Before Deleting Any Branch

- [ ] I have confirmed which branch I'm currently on (`git branch` or `git status`)
- [ ] I am NOT on the branch I plan to delete
- [ ] I have checked `git branch --merged <base-branch>` to see what's safe to delete
- [ ] I have identified protected branches: `main`, `master`, `develop`, `release/*`
- [ ] I have run a dry-run first (echo or print the branches without deleting)

## Before Bulk Deleting

- [ ] I have a clear understanding of the project's branch naming convention
- [ ] I have excluded any branch that might be in active use (check for recent commits <14 days)
- [ ] I have warned teammates if branches they might be using are affected
- [ ] I have backed up important work by pushing to remote if needed

## Protected Branches (Never Delete)

- `main`
- `master`
- `develop`
- `release/*`
- Any branch actively deployed to staging/production

## Danger Signs — Stop Before Deleting

| Red Flag | Action |
|---|---|
| Unmerged branch with recent commits (<7 days) | Ask author before deleting |
| Branch with commits not on any remote | Push to backup remote first |
| Branch with special prefix (hotfix/*, fix/*) | Investigate purpose |
| Branch with active PR open | Check PR status first |
| Shared team branch | Get team consensus |

## Recovery Plan

If you accidentally delete a branch:

```bash
# Find the commit SHA of the branch tip (git reflog survives branch deletion)
git reflog | grep "branch-name"

# Restore it
git branch branch-name <sha>

# Or if you know the approximate time of the last commit
git reflog --date=iso | grep "branch-name"
```

## Branch Age Guidelines

| Age | Status | Recommended Action |
|---|---|---|
| < 7 days | Fresh | Keep unless clearly abandoned |
| 7-30 days | Active | Keep, check with author |
| 30-90 days | Stale | Investigate before deleting |
| > 90 days | Very stale | Likely safe to delete if merged |
| > 90 days, unmerged | Abandoned | Get confirmation, then delete |
