---
name: log-analyzer
description: "Analyze log files for errors, warnings, patterns, and anomalies. Use when: debugging issues, finding error causes, analyzing server logs, parsing application logs, detecting patterns in timestamps, identifying slow requests, or summarizing log dumps. Triggers on: analyze logs, parse log file, find errors in logs, debug from logs, log analysis, error patterns, exception trace, stack trace parsing."
---

# Log Analyzer

Structured log analysis for debugging and pattern detection.

## Quick Analysis Workflow

### Step 1: Categorize the Log

| Log Type | Common Pattern | Tool Focus |
|---|---|---|
| Server (nginx/apache) | IP - - [timestamp] "request" status | Status codes, slow requests |
| Application (Node/Python/Java) | timestamp LEVEL message | Error traces, exceptions |
| System (syslog) | timestamp hostname service | Service failures, OOM |
| Access log | HTTP method, path, status, duration | Slow endpoints, 4xx/5xx |
| Debug trace | Nested indentation, trace IDs | Flow reconstruction |

### Step 2: Extract Errors First

```bash
# Find all errors and warnings
grep -n -E "(ERROR|WARN|Exception|FATAL)" logfile.log

# Find specific error patterns
grep -n -E "(ECONNREFUSED|ETIMEDOUT|ENOTFOUND)" logfile.log

# Get context around errors (3 lines before/after)
grep -n -B3 -A3 "ERROR" logfile.log

# Count errors by type
grep -oE "ERROR: [^\s]+" logfile.log | sort | uniq -c | sort -rn
```

### Step 3: Time-Based Analysis

```bash
# Extract timestamps
grep -oE "\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}" logfile.log | head -5

# Find entries in time range
awk '/2026-03-29T10:/ && /2026-03-29T11:/' logfile.log

# Detect gaps (potential crashes or hangs)
grep -oE "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" logfile.log | awk 'NR>1 && $1!=prev {print "GAP:", prev, "->", $1} {prev=$1}'
```

### Step 4: Pattern Detection

```bash
# Find slow requests (duration > threshold)
grep -oE "duration=[0-9]+" logfile.log | awk -F= '$1>5000 {print}'

# Find repeated failed attempts (auth failures)
grep "Authentication failed" logfile.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head

# Find memory issues
grep -E "(OOM|out of memory|heap|memory)" logfile.log

# Find database slow queries
grep -E "query took [0-9]+ms" logfile.log | awk '{print $NF}' | tr -d 'ms' | awk '$1>1000'
```

### Step 5: Structured Output

```
## Log Analysis Summary

**File:** app.log
**Time Range:** 2026-03-29 08:00 - 12:00
**Total Entries:** 12,847

### Error Summary
| Count | Level | Message Pattern |
|-------|-------|----------------|
| 23 | ERROR | Connection refused |
| 8 | WARN | Rate limit exceeded |
| 3 | ERROR | NullPointerException |

### Timeline
- 08:42 - First error cluster (3 errors in 2 min)
- 09:15 - Service recovered
- 11:30 - Second error cluster (ongoing)

### Root Cause Hypothesis
Database connection pool exhausted due to slow queries.
Connection refused errors follow each slow query.

### Recommended Actions
1. Check database query performance (slow query log)
2. Increase connection pool size
3. Add circuit breaker for DB calls
```

## Multi-File Analysis

```bash
# Combine and sort by timestamp
cat app1.log app2.log app3.log | sort -t'[' -k2 > combined.log

# Find correlation across services using trace IDs
grep "$(cat trace-id-file)" *.log

# Diff two log snapshots
diff <(grep ERROR log-before.log) <(grep ERROR log-after.log)
```

## LogQL-style Patterns (for Loki/Prometheus)

```
# Error rate over time
sum by (level) (count_over_time({job="app"} |~ "ERROR" [5m]))

# Slowest endpoints
topk(5, sum by (path) (rate(http_request_duration_seconds_sum[5m])))
```

## Common Log Format Parsers

```bash
# JSON logs (jq-friendly)
cat log.json | jq '.level, .message, .timestamp'

# Apache/Nginx combined log
awk '{print $1, $7, $9, $10}' access.log

# Kubernetes pod log
kubectl logs -f deployment/app --tail=100 --since=1h

# Docker container logs
docker logs --tail 100 --since "2026-03-29T10:00" container_id
```

## Red Flags

- [ ] Logs suddenly stop (crash or hang)
- [ ] Growing error rate without recovery
- [ ] Memory/CPU logs spike before errors
- [ ] Same error repeating in tight loop (potential bug)
- [ ] Auth failures from multiple IPs (attack)
- [ ] Connection pool exhausted repeatedly
- [ ] Slow queries coinciding with user complaints

## Tools

- `grep` / `rg` — Pattern search
- `awk` — Field extraction and filtering
- `jq` — JSON log parsing
- `sort` / `uniq` — Aggregation
- `tail` / `head` — Sampling
- `diff` — Compare log snapshots
