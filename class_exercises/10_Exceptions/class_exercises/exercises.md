# Class Exercises: Exceptions

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

## Exercise 1: Custom Context Managers

**Description:**
Create custom context managers to handle temporary file operations. You will implement the same functionality using both class-based and decorator-based approaches.

**Requirements:**
- Implement a class-based context manager called `TempFileWriter` that:
  - Accepts a filename in its `__init__` method
  - Opens the file for writing in `__enter__` and returns the file handle
  - Closes the file in `__exit__`
  - Deletes the file in `__exit__` (cleanup)
  - Properly handles exceptions that occur within the context

- Implement a decorator-based context manager called `temp_file_writer` using `@contextmanager` that provides the same functionality as the class-based version

- Both context managers should:
  - Create and open a file for writing
  - Yield the file handle to the caller
  - Ensure the file is closed
  - Delete the file after use (whether the context exits normally or with an exception)

- Include type hints for all functions and methods
- Write at least 3 unit tests for each approach (class-based and decorator-based)
- Tests should verify: normal operation, exception handling, and file cleanup

**Example Usage:**

```python
# Class-based approach
with TempFileWriter("temp.txt") as f:
    f.write("Hello, World!")
    # File exists and is writable here
# File is automatically closed and deleted here

# Decorator-based approach
with temp_file_writer("temp.txt") as f:
    f.write("Hello, World!")
    # File exists and is writable here
# File is automatically closed and deleted here
```

---

## Exercise 2: Custom Exception Hierarchy

**Description:**
Create a custom exception hierarchy for a configuration file parser. Implement functions that raise and handle these custom exceptions appropriately.

**Requirements:**
- Define a base exception class `ConfigError` that inherits from `Exception`
- Define three specific exception classes that inherit from `ConfigError`:
  - `ConfigFileNotFoundError` - raised when config file doesn't exist
  - `ConfigParseError` - raised when config file has invalid format
  - `ConfigValidationError` - raised when config values are invalid

- Implement a function `parse_config(filename: str, required_keys: list[str]) -> dict[str, str]` that:
  - Raises `ConfigFileNotFoundError` if the file doesn't exist
  - Raises `ConfigParseError` if the file format is invalid (should be `key=value` pairs, one per line)
  - Raises `ConfigValidationError` if any required keys are missing
  - Returns a dictionary of configuration key-value pairs if successful
  - Ignores empty lines and lines starting with `#` (comments)

- Include type hints for all functions and classes
- Write at least 3 unit tests covering:
  - Successful parsing
  - Each type of exception being raised
  - Edge cases (empty file, comments, whitespace)

**Example:**

```python
# Valid config file content:
# host=localhost
# port=8080
# # This is a comment
# timeout=30

config = parse_config("app.config", ["host", "port"])
# Returns: {"host": "localhost", "port": "8080", "timeout": "30"}

# If required key "database" is missing:
# Raises ConfigValidationError: Missing required keys: database
```

---

## Exercise 3: Robust File Processing with Exception Handling

**Description:**
Create a robust file processing system that reads a file containing numbers and calculates their average, properly handling various error conditions.

**Requirements:**
- Implement a function `calculate_average_from_file(filename: str) -> dict[str, float | int | str | None]` that:
  - Reads a file where each line contains a number
  - Returns a dictionary with statistics: `{"average": float, "count": int, "error": None}`
  - Handles `FileNotFoundError` and returns `{"average": None, "count": 0, "error": "File not found"}`
  - Handles `ValueError` (invalid number format) and returns `{"average": None, "count": 0, "error": "Invalid number format"}`
  - Handles `PermissionError` and returns `{"average": None, "count": 0, "error": "Permission denied"}`
  - Uses `try-except-else-finally` structure appropriately
  - Skips empty lines
  - Properly closes the file using a context manager

- Implement a function `process_multiple_files(filenames: list[str]) -> dict[str, dict[str, float | int | str | None]]` that:
  - Processes multiple files
  - Returns a dictionary mapping each filename to its results
  - Continues processing remaining files even if one fails
  - Uses the `calculate_average_from_file` function

- Include type hints for all functions
- Write at least 3 unit tests for each function covering:
  - Successful processing
  - Various error conditions
  - Edge cases (empty file, single number, multiple files with mixed success/failure)

**Example:**

```python
# File "numbers.txt" contains:
# 10
# 20
# 30

result = calculate_average_from_file("numbers.txt")
# Returns: {"average": 20.0, "count": 3, "error": None}

result = calculate_average_from_file("missing.txt")
# Returns: {"average": None, "count": 0, "error": "File not found"}

results = process_multiple_files(["numbers.txt", "missing.txt", "more.txt"])
# Returns: {
#     "numbers.txt": {"average": 20.0, "count": 3, "error": None},
#     "missing.txt": {"average": None, "count": 0, "error": "File not found"},
#     "more.txt": {"average": 15.0, "count": 2, "error": None}
# }
```
