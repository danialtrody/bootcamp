# Performance Analysis

## Problem 1 — Blocking I/O Operations

### The code runs I/O operations one after another:

```python
user = fetch_user_data(user_id)
inventory = fetch_inventory_data(product_id)
shipping = fetch_shipping_options(zip_code)
```
### Why is it a problem?
- These operations are independent.
- Running them sequentially increases response time and reduces performance.
### Correct approach
- Run them together using asynchronous execution:
```python
await asyncio.gather()
```


## Problem 2 — CPU Intensive Fibonacci Calculation

### The function:

```python
calculate_fibonacci(FIBONACCI_INDEX)
```
Is a recursive CPU-heavy calculation.

### Why is it a problem?
- CPU tasks block the event loop in Python async applications.

### Correct approach
- Use ThreadPoolExecutor
- Use ProcessPoolExecutor
```python
loop.run_in_executor()
```



## Problem 3 — Blocking Payment Processing Using time.sleep

### The code uses:

```python
time.sleep(PAYMENT_PROCESSING_DELAY)
```
Is a recursive CPU-heavy calculation.

### Why is it a problem?
- time.sleep() blocks the server.
- While sleeping, the server cannot handle other requests.

### Correct approach
- Use:
```python
await asyncio.sleep()
```