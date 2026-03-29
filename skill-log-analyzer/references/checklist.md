# Log Analysis Checklist

## First 5 Minutes
- [ ] Identify log type and format
- [ ] Check log time range
- [ ] Count total entries and error count
- [ ] Find first error timestamp
- [ ] Identify log source/service

## Error Triage
- [ ] Extract all ERROR/FATAL entries
- [ ] Group by error type
- [ ] Find the oldest error (root cause candidate)
- [ ] Check for error clusters (same time = related)

## Correlation
- [ ] Match errors with deployment/events
- [ ] Check resource metrics (CPU/memory/disk)
- [ ] Look for slow query patterns
- [ ] Find connection/resource exhaustion

## Resolution
- [ ] Identify root cause
- [ ] Check if related to recent change
- [ ] Suggest immediate mitigation
- [ ] Recommend long-term fix
