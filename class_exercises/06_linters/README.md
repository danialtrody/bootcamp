# Module 06: Linters and Code Formatters

## Overview

This module teaches students how to use Python linters and code formatters to improve code quality, maintainability, and adherence to best practices through hands-on refactoring exercises.

## Module Contents

- `class_exercises/` - Hands-on refactoring exercises:
  - `exercises.md` - Exercise instructions and requirements
  - `example.py` - A purposefully poorly-written function for students to refactor
  - `setup.cfg` - Linter configuration file (flake8, mypy)
  - `requirements.txt` - Required linter packages
  - `lint.sh` / `lint.ps1` - Scripts to run linters

## Learning Objectives

Students will learn:
- Why code quality tools are important
- How to use `black` for automatic code formatting
- How to use `flake8` with `wemake-python-styleguide` for style checking
- How to use `mypy` for static type checking
- How to interpret and fix linter errors
- How to refactor code systematically using linters as a guide
- Best practices for writing clean, maintainable Python code

## Instructor Guide

### Teaching Approach

This module uses a **learn-by-doing** approach where students refactor poorly-written code using linters as their guide.

### Class Flow

1. **Introduction (10 minutes)**
   - Explain the importance of code quality
   - Introduce the three main tools: black, flake8, mypy
   - Show examples of good vs. bad code

2. **Setup (10 minutes)**
   - Guide students through copying linter configuration files
   - Install linter packages in virtual environment
   - Run initial linters to see the "before" state

3. **Hands-on Exercise (60-90 minutes)**
   - Students work through Exercise 1: refactoring `example.py`
   - Encourage systematic approach:
     1. Run black formatting first
     2. Add type hints
     3. Fix variable names
     4. Address remaining flake8 warnings
     5. Break into smaller functions if needed
   - Walk around and help students interpret linter messages

4. **Review and Discussion (15-20 minutes)**
   - Discuss common patterns students encountered
   - Show example of well-refactored solution
   - Highlight key takeaways

5. **Optional Challenge (If time permits)**
   - Students attempt Exercise 2: writing clean code from scratch

### Key Teaching Points

**Why Linters Matter:**
- Catch bugs before runtime (mypy)
- Enforce consistent style across team (black, flake8)
- Identify complex code that's hard to maintain (wemake complexity checks)
- Automated code review that never gets tired

**Common Student Challenges:**
- **Type hints confusion**: Explain when to use `list[int]` vs `list[float]` vs `list[int | float]`
- **Too many variables**: Guide students to break functions apart or use dataclasses
- **Fear of breaking working code**: Emphasize running tests after each change
- **Ignoring vs. fixing**: Stress the "no ignore directives" policy

**Demonstrating Value:**
- Show the same code before and after refactoring side-by-side
- Point out how much easier refactored code is to understand
- Explain how this scales to large codebases with many developers

### Initial Issues in example.py

When students first run linters, they will encounter:

**Black:**
- Formatting inconsistencies (will auto-fix)

**Flake8 + wemake-python-styleguide:**
- `WPS210` - Too many local variables: 9 > 8
- `WPS111` - Too short names: t, c, p, f, h, l, s, a (multiple occurrences)
- `WPS350` - Usable augmented assign patterns

**Mypy:**
- `no-untyped-def` - Function is missing type annotations

### Example Refactoring Path

Show students one possible refactoring approach:

1. **Black formatting** → Automatic fixes
2. **Add type hints** → `def calculate_test_statistics(scores: list[int | float]) -> dict[str, float | int]:`
3. **Rename variables** → All single-letter names become descriptive
4. **Use augmented assignments** → Change `t = t + s` to `t += s`
5. **Reduce variables** → Extract helper functions or use built-ins like `max()`, `min()`, `sum()`

### Troubleshooting

**"My mypy is still failing!"**
- Check that type hints cover parameters AND return type
- Verify return dictionary keys match type annotations
- Consider using `TypedDict` for complex return types

**"I still have too many local variables!"**
- Break into smaller functions (e.g., `find_min_max()`, `count_passing()`)
- Use Python built-ins: `sum()`, `len()`, `max()`, `min()`
- Return a dataclass instead of dictionary

**"The tests are failing after refactoring!"**
- Run tests after each small change to isolate issues
- Check edge cases (empty list, single item)
- Verify the logic wasn't accidentally changed

## Additional Resources

For detailed linter configuration and standards:
- `linter-config/README_LINTERS.md` - Complete documentation on bootcamp linting standards

External Resources:
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Black Documentation](https://black.readthedocs.io/)
- [Wemake Python Styleguide](https://wemake-python-styleguide.readthedocs.io/)
- [Mypy Documentation](https://mypy.readthedocs.io/)

## Notes

- Solutions for class exercises are stored in `modules/solutions_for_class_exercises/module_06/`
- Students should complete exercises in their own working directories
- Emphasize the "no ignore directives" policy throughout the exercise
