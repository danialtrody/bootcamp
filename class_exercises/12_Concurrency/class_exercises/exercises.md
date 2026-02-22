# Class Exercises: Concurrency

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission.
  - Pass `mypy` type checks before submission.

---

## Exercise 1: Concurrent Fetching of TODO Items

**Description:**
Implement three Python programs that fetch TODO items from the JSONPlaceholder API concurrently. Each program will use a different concurrency approach to fetch 20 TODO items and print their titles. This exercise demonstrates the differences between threading, multiprocessing, and asyncio approaches to concurrency.

**Learning Objectives:**
- Understand different concurrency models in Python
- Compare thread-based, process-based, and async-based concurrency
- Work with external APIs using different HTTP libraries
- Measure and compare performance across different approaches

**API Information:**
- Base URL: `https://jsonplaceholder.typicode.com/todos/<number>`
- Replace `<number>` with TODO item IDs from 1 to 20
- Example: `https://jsonplaceholder.typicode.com/todos/1`
- Each request returns a JSON object with fields: `id`, `title`, `completed`, `userId`

**Common Requirements for All Programs:**
- Fetch TODO items with IDs from 1 to 20 (20 total items)
- Print the title of each TODO item as it's fetched
- Measure and display the total execution time
- Handle potential errors gracefully (network errors, invalid responses)
- Include type hints for all functions
- Add a `if __name__ == "__main__":` guard for the main execution

---

### Part 1: ThreadPoolExecutor Implementation

**Requirements:**
- Create a program named `fetch_todos_threading.py`
- Use `concurrent.futures.ThreadPoolExecutor` for concurrency
- Use the `requests` library for HTTP requests (you'll need to install it: `pip install requests`)
- Create a function `fetch_todo(todo_id: int) -> dict[str, Any]` that fetches a single TODO item
- Use ThreadPoolExecutor with `max_workers=8` to fetch all 20 items concurrently
- Print each TODO title as it's received
- Measure execution time using `time.time()`
- Print summary statistics: total time, average time per request

**Example Output:**
```
Fetching 20 TODO items using ThreadPoolExecutor...
TODO 3: fugiat veniam minus
TODO 1: delectus aut autem
TODO 2: quis ut nam facilis et officia qui
TODO 5: laboriosam mollitia et enim quasi adipisci quia provident illum
...
TODO 20: ullam nobis libero sapiente ad optio sint

Summary:
Total execution time: 0.85 seconds
Average time per request: 0.043 seconds
```

**Hints:**
- Use `executor.submit()` to submit tasks and collect futures
- Use `concurrent.futures.as_completed()` to process results as they complete

---

### Part 2: ProcessPoolExecutor Implementation

**Requirements:**
- Create a program named `fetch_todos_multiprocessing.py`
- Use `concurrent.futures.ProcessPoolExecutor` for concurrency
- Use the `requests` library for HTTP requests
- Create a function `fetch_todo(todo_id: int) -> dict[str, Any]` that fetches a single TODO item
- Use ProcessPoolExecutor with `max_workers=8` to fetch all 20 items concurrently
- Print each TODO title as it's received
- Measure execution time and print summary statistics

**Important Notes:**
- ProcessPoolExecutor creates separate Python processes, which have more overhead than threads
- For I/O-bound tasks like HTTP requests, ProcessPoolExecutor is typically **not** the best choice
- This exercise helps you understand when **not** to use multiprocessing
- Compare the performance with the threading version

**Example Output:**
```
Fetching 20 TODO items using ProcessPoolExecutor...
TODO 1: delectus aut autem
TODO 2: quis ut nam facilis et officia qui
TODO 4: et porro tempora
...
TODO 20: ullam nobis libero sapiente ad optio sint

Summary:
Total execution time: 1.23 seconds
Average time per request: 0.062 seconds
```

