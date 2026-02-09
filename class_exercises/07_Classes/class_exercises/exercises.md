# Class Exercises: Classes

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
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

## Exercise 2: Vector Class with Operator Overloading

**Description:**
Create a `Vector2D` class that represents a 2D vector and implements various dunder methods for operator overloading. This will help you understand how Python's special methods work and how to make your classes behave like built-in types.

**Note:** You can disalbe the rule for short variavle names for this exercise.

**Requirements:**
- Create a `Vector2D` class with:
  - Instance attributes: `x` (float), `y` (float)
  - `__init__(self, x: float, y: float)` - constructor
  - `__str__(self) -> str` - returns string representation like "Vector2D(3.0, 4.0)"
  - `__repr__(self) -> str` - returns the same as `__str__`
  - `__eq__(self, other: object) -> bool` - checks if two vectors are equal
  - `__add__(self, other: "Vector2D") -> "Vector2D"` - adds two vectors
  - `__sub__(self, other: "Vector2D") -> "Vector2D"` - subtracts two vectors
  - `__mul__(self, scalar: float) -> "Vector2D"` - multiplies vector by a scalar
  - `__abs__(self) -> float` - returns the magnitude (length) of the vector
  - `magnitude(self) -> float` - returns the magnitude using the Pythagorean theorem
  - `dot(self, other: "Vector2D") -> float` - returns the dot product of two vectors

- The `__eq__` method should handle comparison with non-Vector2D objects gracefully (return False)
- Include comprehensive type hints for all methods
- Write at least 3 unit tests that verify:
  - Operator overloading works correctly
  - Comparison and equality work as expected
  - Edge cases (zero vector, negative components, etc.) are handled

**Example:**

```python
v1 = Vector2D(3.0, 4.0)
v2 = Vector2D(1.0, 2.0)

print(v1 + v2)  # Output: Vector2D(4.0, 6.0)
print(v1 - v2)  # Output: Vector2D(2.0, 2.0)
print(v1 * 2)   # Output: Vector2D(6.0, 8.0)
print(abs(v1))  # Output: 5.0
print(v1.dot(v2))  # Output: 11.0
print(v1 == Vector2D(3.0, 4.0))  # Output: True
```

---

## Exercise 3: BankAccount with Properties and Encapsulation

**Description:**
Design and implement a `BankAccount` class that demonstrates proper use of properties, encapsulation, and validation. Your class should protect account data from invalid modifications while providing a clean interface for banking operations.

**Learning Objectives:**
- Use properties to control access to class attributes
- Implement encapsulation with private attributes
- Add validation logic to enforce business rules
- Raise appropriate exceptions for invalid operations

**Requirements:**
- Design a `BankAccount` class that supports basic banking operations (deposits, withdrawals, balance inquiries)
- Protect sensitive account data from direct modification outside the class
- Prevent invalid operations such as:
  - Depositing or withdrawing negative or zero amounts
  - Withdrawing more money than available in the account
- Track useful information about the account's activity
- Provide a way to view account information in a user-friendly format

**Design Considerations:**
- What attributes should be private vs. public?
- Which attributes should be read-only, and which should be modifiable?
- What methods are needed for safe account operations?
- How should invalid operations be handled (exceptions, return values)?
- What validation rules make sense for a bank account?

**Testing Requirements:**
- Write at least 3 comprehensive unit tests that verify:
  - Encapsulation: Protected data cannot be modified directly
  - Validation: Invalid operations are properly rejected
  - Business logic: Account operations work correctly under various scenarios

**Example Usage:**
Your implementation should support usage similar to this (exact method names and behavior are up to you):

```python
account = BankAccount("ACC123456")  # Create account with initial balance of 0

# Deposit money
account.deposit(1000.0)
print(account.balance)  # Should show 1000.0

# Withdraw money
account.withdraw(300.0)
print(account.balance)  # Should show 700.0

# Attempt invalid withdrawal (should raise an exception)
account.withdraw(800.0)  # Should fail - insufficient funds

# Attempt to modify balance directly (should fail)
account.balance = 5000.0  # Should raise an error - balance is protected

# View account information
print(account.get_statement())  # Display account details
```

**Note:** The exact implementation is up to you. Focus on proper encapsulation, validation, and creating a clean, intuitive interface.