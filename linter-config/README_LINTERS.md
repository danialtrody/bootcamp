# Linters Config for Bootcamp 2026

## Overview

This directory contains the **official style guide and linting configuration** for the Codevalue Python Bootcamp 2026. All students and instructors must use these configurations to ensure consistent code quality and adherence to Python best practices throughout the bootcamp.

## Tools and Standards

This configuration enforces code quality using three complementary tools:

1. **flake8** - Basic rules, PEP 8 style guide enforcement
2. **wemake-python-styleguide** - Strict flake8 plugin for code quality and complexity management
3. **mypy** - Static type checker requiring type annotations on all function and method declarations

## Contents

- `setup.cfg` - Configuration file for flake8, wemake-python-styleguide, and mypy
- `requirements.txt` - Python packages needed for linting
- `lint.sh` - Shell script to run linters (Unix/Linux/macOS)
- `lint.ps1` - PowerShell script to run linters (Windows)

## Setup Instructions

### 1. Install Linting Tools

From your project directory (with virtual environment activated):

```bash
# Unix/Linux/macOS
source venv/bin/activate && pip install -r requirements.txt

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

### 2. Copy Configuration to Your Project

Copy the `setup.cfg` file to the root of your project directory:

```bash
# Unix/Linux/macOS
cp linter-config/setup.cfg .

# Windows (PowerShell)
Copy-Item linter-config\setup.cfg .
```

## Running the Linters

### Option 1: Use the Provided Scripts

**Unix/Linux/macOS:**
```bash
source venv/bin/activate && bash linter-config/lint.sh
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1; .\linter-config\lint.ps1
```

### Option 2: Run Manually

With virtual environment activated:

```bash
# Run flake8 with wemake-python-styleguide
flake8 . --select=WPS

# Run mypy type checker
mypy --exclude-gitignore .
```

**CRITICAL**: All function and method declarations must include type hints for:
- All parameters
- Return values

### Limited Suppression Comments

**AVOID** using linter suppression comments to bypass errors:
- ❌ `# type: ignore` (mypy)
- ❌ `# noqa` (flake8)
- ❌ Any other suppression directives

Using these comments to silence errors require instructor approval. Will be approved only in a very exceptional case where the error cannot be resolved through proper code refactoring or type annotation. WPS limits the number of suppression comments.

If you encounter linter errors, fix the underlying issue properly by refactoring the code, adding proper type annotations, or restructuring the logic.

### During Code Review

Instructors will use these same tools to review submissions. Code that doesn't pass these checks will need to be revised before approval.

## Support

If you encounter linter issues you cannot resolve:
1. Review the specific error message and rule documentation
2. Run `wps explain <error code>` (when venv is active)
3. Consult the [wemake-python-styleguide documentation](https://wemake-python-styleguide.readthedocs.io/)

## Additional Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [wemake-python-styleguide Documentation](https://wemake-python-styleguide.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Type Hints in Python](https://docs.python.org/3/library/typing.html)
