# Common Git Branch One-Liners

## Quick Reference (Copy-Paste Ready)

### List & Inspect
```bash
# All local branches sorted by most recent commit
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/

# Branches with authors
git for-each-ref --sort=-committerdate --format='%(authorname) %(committerdate:short) %(refname:short)' refs/heads/

# Remote branches only
git branch -r

# Show tracking status for all branches
git branch -vv
```

### Find Stale Branches
```bash
# Not updated in 30 days
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(committerdate:relative)' refs/heads/ | awk '$1 <= "'$(date -d "30 days ago" +%Y-%m-%d)'"'

# Branches with no upstream (never pushed or deleted remote)
git branch -vv | grep -v ': ahead\|: behind\|: gone'

# Branches tracking a deleted remote
git branch -vv | grep ': gone'
```

### Merge Status
```bash
# All merged into current branch
git branch --merged

# All merged into main
git branch --merged main

# All NOT merged into main
git branch --no-merged main

# Merged branches excluding protected ones
git branch --merged main | grep -v -E '(main|master|develop|\*)'
```

### Delete Safely
```bash
# Dry run - show merged branches to delete
git branch --merged main | grep -v -E '(main|master|develop|\*)'

# Interactive delete (macOS)
git branch --merged main | grep -v -E '(main|master|develop|\*)' | fzf -m | xargs git branch -d

# PowerShell: show merged branches to delete
git branch --merged main | Where-Object { $_ -notmatch '(main|master|develop|\*)' }
```

### Compare Branches
```bash
# Show commits in feature but not in main
git log main..HEAD --oneline

# Show commits in main but not in feature
git log HEAD..main --oneline

# Diff stats between branches
git diff --stat main..HEAD

# Full diff between branches
git diff main..HEAD

# Files changed between branches
git diff --name-only main..HEAD
```

### Archive Old Branches (Instead of Deleting)
```bash
# Create an archive tag before deleting
git tag archive/<branch-name> <branch-name>

# Then delete the branch
git branch -d <branch-name>
```

### Rename
```bash
# Rename current branch
git branch -m new-name

# Rename a specific branch
git branch -m old-name new-name

# Push new name and delete old remote
git push origin :old-name new-name
git push origin -u new-name
```

### Sync & Prune
```bash
# Fetch and prune in one command
git fetch --prune

# Prune all stale remote tracking branches
git remote prune origin

# Check what would be pruned (dry run)
git remote prune origin --dry-run
```

## Platform-Specific

### Windows/PowerShell: Stale branches (60 days)
```powershell
$cutoff = (Get-Date).AddDays(-60).ToString('yyyy-MM-dd')
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/ | Where-Object { $_.Split(' ')[0] -le $cutoff }
```

### macOS/Linux: Delete branches older than date
```bash
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/ | awk '$1 <= "2026-01-01"' | xargs -I {} git branch -D {}
```
