# Class Exercises: Testing Basics

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
- Advice: Write parameterized tests using the `@pytest.mark.parametrize` decorator.
- All the unit tests should be in a Python package called `tests`. Use a separate Python module for each exercise test suite.
- The unit test module should be called by convention `test_<subject>.py`
- Adhere to Python coding standards PEP-8
- Use Type Hints for function arguments and return values
- If the functions is long (beyond 15 lines of code), divide into more functions.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission. Use `wps explain <error code>` to understand the error and how to write correctly.
  - Pass `mypy` type checks before submission.
- Navigate to the `linter-config` directory to find the `setup.cfg` file with the linters configuration. Copy all files to the root of your exercise directory to use the same configuration for your exercises.

---

## Exercise 1: Testing API Calls with Mock Responses

**Description:**
Create a function that fetches TODO items from a public API and processes them. Then write comprehensive tests using the `responses` library to mock HTTP calls without making actual network requests.

**Requirements:**
- Install the required libraries: `requests` and `responses` (they should already be in your requirements.txt)
- Implement a function `fetch_sorted_todos(limit: int = 20) -> list[dict[str, Any]]` that:
  - Fetches TODO items from `https://jsonplaceholder.typicode.com/todos/<number>` where `<number>` goes from 1 to `limit`
  - Returns a list of TODO items sorted alphabetically by the "title" field
  - Each TODO item should be a dictionary with keys: "id", "userId", "title", "completed"
- Write unit tests using the `responses` library to mock the HTTP calls:
  - Test successful fetching and sorting of TODOs
  - Test handling of HTTP errors (404, 500)
  - Test with different limit values
  - Use `@pytest.mark.parametrize` where appropriate
- Include proper type hints (use `from typing import Any` for flexibility)

**Note:** For this exercise, passing `mypy` type checking for the test file is **not mandatory**. The `responses` library does not have type stubs available, which causes mypy errors in test code. However, your implementation code (the `fetch_sorted_todos` function) must still pass `mypy --strict` checks. The focus is on learning proper testing practices with the `responses` library. Your solution should pass `black` and `flake8` checks for all files.

**API Endpoint Format:**
```
https://jsonplaceholder.typicode.com/todos/1
https://jsonplaceholder.typicode.com/todos/2
...
```

**Example Response:**
```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

