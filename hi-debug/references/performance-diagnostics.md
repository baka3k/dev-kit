# Performance Diagnostics

Identify bottlenecks, analyze query performance, and develop optimization strategies.

**Use when:** response times increased significantly, app feels slow, DB queries taking too long, high CPU/memory/disk, resource exhaustion or OOM.

## 1. Quantify the Problem

**Measure before optimizing.** Establish expected vs actual response time, when degradation started (correlate with changes), which endpoints are affected, and whether it's consistent or intermittent.

## 2. Identify the Bottleneck Layer

```
Request → Network → Web Server → Application → Database → Filesystem
                                      ↓
                              External APIs / Services
```

**Elimination approach:** measure time at each layer.

| Layer | Check | Tool |
|-------|-------|------|
| Network | Latency, DNS, TLS | `curl -w` timing, network logs |
| Web server | Request queue, connections | Server metrics, access logs |
| Application | CPU profiling, memory | Profiler, APM, `process.memoryUsage()` |
| Database | Query time, connections | `EXPLAIN ANALYZE`, `pg_stat_statements` |
| Filesystem | I/O wait, disk usage | `iostat`, `df -h` |
| External APIs | Response time, timeouts | Request logging with durations |

## 3. Database Performance

```sql
-- Slow queries (requires pg_stat_statements)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;

-- Active queries right now
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC;

-- Table sizes and bloat
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC LIMIT 20;

-- Missing indexes (sequential scans on large tables)
SELECT relname, seq_scan, seq_tup_read, idx_scan
FROM pg_stat_user_tables WHERE seq_scan > 100 AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;

-- Connection pool status
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Analyze specific query execution plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <your-query>;
```

Look for: sequential scans on large tables, nested loops with high row counts, sorts without indexes, excessive buffer hits.

## 4. Application Performance

| Issue | Symptom | Fix |
|-------|---------|-----|
| N+1 queries | Many small DB calls per request | Eager loading, batch queries |
| Memory leaks | Growing memory over time | Profile heap, check event listeners |
| Blocking I/O | High response time, low CPU | Async operations, connection pooling |
| CPU-bound | High CPU, proportional to load | Optimize algorithms, caching |
| Connection exhaustion | Intermittent timeouts | Pool sizing, connection reuse |
| Large payloads | Slow transfers, high memory | Pagination, compression, streaming |

## 5. Optimization Strategy

**Priority order:** quick wins (add missing index, fix N+1, enable caching) → configuration (pool sizes, timeouts, worker counts) → code changes (algorithms, data structures) → architecture (caching, read replicas, async, CDN). Always measure after each change; one change at a time.

## Reporting Performance Issues

Include in diagnostic report: baseline vs current metrics (with numbers), bottleneck identification with evidence, root cause explanation, recommended fixes with expected impact, verification plan to confirm improvement.
