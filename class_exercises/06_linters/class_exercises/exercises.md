# Class Exercises: Linters and Code Quality

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

## Setup: Installing and Configuring Linters

Before starting the exercises, you need to set up the linting tools.

### 2. Install Linter Packages

Install the required linter tools in your virtual environment:

```bash
# Activate your virtual environment first
source venv/bin/activate  # Linux/Mac
# or
source venv/Scripts/activate  # Windows (Git Bash)

# Install linter dependencies
pip install -r requirements.txt
```

This will install:
- **black** - Automatic code formatter
- **flake8** - Style checker
- **wemake-python-styleguide** - Strict flake8 plugin for best practices
- **mypy** - Static type checker

### 3. Running Linters

You can run the linters individually or use the provided script:

**Individual commands:**
```bash
# Format code with black
black <file_or_directory>

# Check formatting without changing files
black --check <file_or_directory>

# Run flake8 with wemake-python-styleguide
flake8 <file_or_directory> --select=WPS

# Run mypy type checker
mypy <file_or_directory>
```

**Using the convenience script:**
```bash
# Linux/Mac
./lint.sh

# Windows PowerShell
.\lint.ps1
```

### 4. Understanding Linter Output

Each linter will report issues with:
- **File location**: `file.py:line:column`
- **Error code**: e.g., `WPS111`, `WPS210`
- **Description**: What the issue is

**Example output:**
```
example.py:36:5: WPS111 Found too short name: t < 2
example.py:6:1: WPS210 Found too many local variables: 9 > 8
```

### 5. Using `wps explain` for Detailed Error Information

When you encounter a wemake-python-styleguide error, use the `wps explain` command to get detailed information about why it's an issue and how to fix it:

```bash
# Get explanation for a specific error code
wps explain WPS111
```

**Example Output:**
```
WPS111 ✘ Forbid short variable or module names.

Reasoning:
    It is hard to understand what the variable means and why it is used,
    if its name is too short.

Solution:
    Think of another name. Give more context to it.

Example::

    # Correct:
    x_coordinate = 1
    abscissa = 2

    # Wrong:
    x = 1
    y = 2

See at website: https://pyflak.es/WPS111
```

The `wps explain` output provides:
- **Reasoning**: Why this rule exists and why it's important
- **Solution**: How to fix the issue properly
- **Examples**: Code showing both correct and wrong approaches
- **Website Link**: Link to full documentation with more details

**Try it with other error codes:**
```bash
wps explain WPS210  # Too many local variables
wps explain WPS350  # Augmented assignment pattern
```

For detailed information about linter configuration and standards, see the `linter-config/README_LINTERS.md` file in the repository root.

---

## Exercise 1: Refactor Code Using Linters

**Description:**
You are provided with a working but poorly-written Python function in `example.py`. The function calculates statistics for a list of test scores, but it violates many Python best practices and coding standards. Your task is to refactor this code step-by-step, using linters as your guide to improve code quality.

**Initial Code:**
The `example.py` file contains the function `calculate_test_statistics()` that works correctly but has numerous code quality issues including:
- Missing type hints
- Poor variable naming (single-letter names)
- Too many local variables
- Inefficient patterns (e.g., `x = x + 1` instead of `x += 1`)
- No separation of concerns

**Your Task:**
Refactor the code to pass all linter checks **without using any ignore directives** (`# type: ignore`, `# noqa`, etc.). You must fix the underlying issues properly.

**Requirements:**

1. **Cover with Unit Tests** - Create comprehensive tests in `tests/test_statistics.py`:
   - Test normal cases with various score lists
   - Test edge cases (empty list, single score, all passing, all failing)
   - Test boundary conditions (scores at 60, 0, 100)
   - Aim for at least 5 different test cases

2. **Run the Initial Linters** - Before starting, run all three linters to see what issues exist:
   ```bash
   black example.py
   flake8 example.py --select=WPS
   mypy example.py
   ```

3. **Apply Black Formatting** - Start by formatting the code:
   ```bash
   black example.py
   ```

4. **Add Type Hints** - Add proper type annotations:
   - Add type hints for the function parameter
   - Add return type annotation
   - Use appropriate types from the `typing` module if needed
   - Make sure `mypy` passes without errors

5. **Fix Variable Names** - Replace cryptic single-letter variable names with descriptive names:
   - `t` → `total`
   - `c` → `count`
   - etc...

6. **Fix Code Quality Issues** - Address flake8 warnings:
   - Use augmented assignment operators (`+=`, `-=`) where appropriate
   - Consider breaking the function into smaller helper functions if needed
   - etc...

7. **Improve Code Structure** (Optional but Recommended):
   - Extract logic into helper functions with clear responsibilities
   - Use constants for magic numbers

8. **Verify All tests and Linters Pass**:
   black .
   flake8 example.py --select=WPS
   mypy example.py

   - Note: Your tests also must pass linter checks.

**Expected Outcome:**
- The function still produces the same results as the original
- All linter checks pass without any ignore directives
- Code is readable, maintainable, and follows Python best practices
- Comprehensive unit tests verify the functionality

**Hints:**
- Start with the easiest fixes first (formatting, variable names)
- Use `wps explain <error_code>` to understand what each flake8 error means and how to fix it properly
- If you have too many local variables, consider:
  - Breaking the function into smaller functions (e.g., `calculate_average`, `find_min_max`, `count_passing`)
- Run linters frequently to see your progress
- The function currently works correctly - make sure it still produces the same results after refactoring
