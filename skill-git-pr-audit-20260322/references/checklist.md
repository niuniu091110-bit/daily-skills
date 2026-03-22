# PR Audit Checklist

## Pre-Review

- [ ] Understand the PR's purpose from description
- [ ] Check CI/CD status (all checks passing?)
- [ ] Note PR size (files changed, additions, deletions)
- [ ] Check if PR is up to date with base branch

## Code Quality

### General
- [ ] Code is readable and self-documenting
- [ ] No commented-out dead code
- [ ] No debug statements or console.logs left in
- [ ] Naming is descriptive and consistent with codebase

### Security
- [ ] No hardcoded credentials, API keys, or secrets
- [ ] User input properly sanitized/validated
- [ ] Auth/permission checks in place
- [ ] No SQL injection vulnerabilities
- [ ] No command injection vulnerabilities
- [ ] Sensitive data not logged

### Error Handling
- [ ] Errors handled explicitly, not silently ignored
- [ ] Appropriate error types used
- [ ] Errors logged for debugging (no sensitive data)
- [ ] Fallback/graceful degradation when possible

### Performance
- [ ] No N+1 query patterns
- [ ] No unnecessary loops or repeated computations
- [ ] Large data processed in chunks if needed
- [ ] Caching used where appropriate

## Testing

- [ ] Tests added for new functionality
- [ ] Existing tests still pass
- [ ] Tests cover happy path AND edge cases
- [ ] Tests are deterministic (no flaky tests)
- [ ] Mocking is realistic and appropriate

## Business Logic

- [ ] Logic correctly implements intended behavior
- [ ] Edge cases handled
- [ ] Validation rules enforced
- [ ] Data integrity maintained
- [ ] No unintended side effects

## API / Contracts

- [ ] API changes are backward compatible
- [ ] Request/response shapes documented
- [ ] Proper HTTP status codes used
- [ ] Pagination handled for list endpoints
- [ ] Error responses are informative

## Database / Migrations

- [ ] Migrations are reversible
- [ ] Migrations are idempotent
- [ ] No data loss scenarios
- [ ] Indexes added for new queries
- [ ] Large migrations consider zero-downtime

## Configuration / Environment

- [ ] No environment-specific hardcoded values
- [ ] Feature flags used for risky changes
- [ ] Config changes documented

## Documentation

- [ ] Code comments explain "why", not "what"
- [ ] Public APIs documented
- [ ] README updated if needed
- [ ] Breaking changes noted in CHANGELOG

## Reviewer Experience

- [ ] PR description is clear and complete
- [ ] Changes are logically organized
- [ ] Related changes grouped together
- [ ] Large changes broken into digestible commits
