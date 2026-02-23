# Performance Results Comparison

## Original Version (app.py)

```
Total time: 29.56 seconds
Average response time: 17.59 seconds
Requests per second: 0.68
```
### Performance Analysis
- The server processed requests slowly.
- Blocking I/O operations and CPU intensive tasks slowed performance.
- Requests were processed almost sequentially.
---

## Optimized Version (app_optimized.py)
```
Total time: 1.63 seconds
Average response time: 1.14 seconds
Requests per second: 12.24
```
### Performance Analysis
- The server processed requests much faster.
- Blocking operations were removed.
- CPU intensive tasks were moved to background execution using executors.
- Asynchronous concurrency improved performance significantly.

---

## Performance Improvements

### Response Time Improvement
- 17.59s → 1.14s  
- Approximately **93% faster**

### Throughput Improvement
- 0.68 requests/sec → 12.24 requests/sec  
- Approximately **18x more requests per second**

---