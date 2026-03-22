---
name: git-pr-audit
description: "Audit GitHub pull requests systematically before merging. Use when reviewing PRs, checking code quality, analyzing risks, writing PR summaries, or responding to review comments. Triggers on: review this PR, audit PR, check this pull request, PR review, analyze PR, summarize changes, check for risks, review comments."
---

# Git PR Audit

Systematic PR review with risk assessment, comment analysis, and actionable feedback.

## Quick Audit

For fast audits, run the checklist mentally:
1. **Scope creep?** New files > 20% of existing or unrelated changes
2. **Risk files?** Models, auth, payment, core business logic
3. **Test coverage?** Tests added/updated alongside code changes
4. **Breaking changes?** API, schema, or contract changes without deprecation
5. **Secrets?** Credentials, keys, or tokens accidentally committed
6. **Comments?** TODO/FIXME/HACK that signals incomplete work

## Deep Audit Workflow

### Step 1: Fetch PR Details

Use `gh` CLI or GitHub API:

```bash
# Get PR metadata
gh pr view <number> --repo <owner/repo> --json title,body,state,author,additions,deletions,changedFiles,mergeable

# Get file list
gh pr diff <number> --repo <owner/repo> --stat

# Get recent commits
gh pr view <number> --repo <owner/repo> --json commits
```

### Step 2: Analyze Each Changed File

For each changed file, check:
- **Business logic files** → Verify correctness, edge cases, error handling
- **API/routes** → Check validation, auth, response shapes
- **Config/env** → No hardcoded secrets, sensible defaults
- **Tests** → Coverage, edge cases, mocking correctness
- **Migration files** → Reversible, idempotent, backward compatible

### Step 3: Risk Scoring

Rate each file: Low / Medium / High / Critical

| Risk Level | Criteria |
|---|---|
| Critical | Auth, payment, data deletion, security configs |
| High | Core business logic, data models, API contracts |
| Medium | Feature logic, UI components, non-critical services |
| Low | Docs, tests, configs, minor fixes |

### Step 4: Write Review Summary

Structure:
```
## Summary
Brief description of what this PR does.

## Changes
- Added: X
- Changed: Y  
- Fixed: Z

## Risk Assessment
- [High] file1.ts - Reason
- [Low] file2.ts - Reason

## Recommendations
1. Suggestion 1
2. Suggestion 2

## Approval
✅ Approve / 🛑 Request Changes / ⏳ Approve with Comments
```

## Handling Review Comments

**Responding to author:**
- Be specific: cite line numbers, link to docs
- Explain the "why" not just the "what"
- Offer alternatives, not just objections
- Distinguish blocking vs. non-blocking feedback

**Categorizing comments:**
- `blocker` — Must fix before merge
- `nit` — Style/preference, non-blocking
- `question` — Seeking understanding
- `suggestion` — Improvement idea, non-blocking
- `praise` — Good work, acknowledge it

## Common Red Flags

- [ ] No tests for new functionality
- [ ] Magic numbers/strings without constants
- [ ] Catching broad exceptions (`except:`)
- [ ] Synchronous blocking calls in async code
- [ ] Missing input validation
- [ ] Insecure direct SQL/command construction
- [ ] Credentials or keys in code
- [ ] Undocumented API changes
- [ ] Breaking changes without migration path
- [ ] Large PRs (>500 lines changed) without clear logical chunks

## Tools

- `gh pr diff` — View file changes
- `gh pr checks` — View CI/CD status
- `gh api` — Raw API for complex queries
- See `references/checklist.md` for printable checklist
