# Exercises 5: Classes & Data structures

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


## Exercise 1: E-commerce System with Multiple Inheritance

**Description:**
Create a class hierarchy that demonstrates multiple inheritance in a real-world e-commerce scenario. You'll implement classes that handle different aspects of an online store: inventory management, discount pricing, and shipping calculations. The final `Product` class will inherit from multiple base classes and override methods appropriately.

**Requirements:**
- Create a base class `Item` with:
  - Instance attributes: `name` (str), `base_price` (float), `weight` (float in kg)
  - Method `get_info() -> str` that returns a formatted string with item details

- Create a mixin class `DiscountMixin` with:
  - Instance attribute: `discount_percent` (float, default 0)
  - Method `get_price() -> float` that returns the price after applying discount

- Create a mixin class `ShippingMixin` with:
  - Class attribute: `shipping_rate_per_kg` = 5.0 (dollars per kg)
  - Method `get_shipping_cost() -> float` that calculates shipping based on weight

- Create a class `Product` that inherits from `Item`, `DiscountMixin`, and `ShippingMixin`:
  - Override the `get_info()` method to include discount and shipping information
  - Implement a method `get_total_cost() -> float` that returns price + shipping
  - The constructor should accept: name, base_price, weight, and optional discount_percent

- Create a class `DigitalProduct` that inherits from `Item` and `DiscountMixin` only:
  - Override `get_info()` to mention it's a digital product (no shipping)
  - The constructor should accept: name, base_price, and optional discount_percent
  - Weight should be set to 0.0

- Include comprehensive type hints for all methods
- Write at least 3 unit tests that verify:
  - MRO (Method Resolution Order) works correctly
  - Method overriding functions as expected
  - Different combinations of inherited behavior work correctly

**Example:**

```python
# Physical product with discount
laptop = Product("Laptop", 1000.0, 2.5, discount_percent=10)
print(laptop.get_price())  # Output: 900.0
print(laptop.get_shipping_cost())  # Output: 12.5
print(laptop.get_total_cost())  # Output: 912.5
print(laptop.get_info())
# Output: "Product: Laptop, Price: $900.00, Shipping: $12.50, Total: $912.50"

# Digital product (no shipping)
ebook = DigitalProduct("Python Guide", 29.99, discount_percent=20)
print(ebook.get_price())  # Output: 23.992
print(ebook.get_info())
# Output: "Digital Product: Python Guide, Price: $23.99 (no shipping)"
```

---

## Exercise 2: Employee Management System with Single Inheritance

**Description:**
Design and implement an employee management system that demonstrates single inheritance. Your system should model different types of employees in a company, where specialized employee types inherit from more general ones. The inheritance hierarchy should reflect real-world organizational structures.

**Learning Objectives:**
- Understand and implement single inheritance hierarchies
- Practice method overriding and extension in subclasses
- Use `super()` to call parent class methods
- Design class hierarchies that reflect real-world relationships
- Implement polymorphism through inheritance

**Requirements:**
- Create a class hierarchy with 2-3 levels of inheritance (no more than 3 levels)
- The base class should represent a general employee with common attributes and behavior
- Derived classes should represent more specialized types of employees
- Each level of inheritance should add or modify behavior appropriately
- Demonstrate at least one case of:
  - Method overriding (child class replaces parent method completely)
  - Method extension (child class calls parent method and adds additional behavior)
- All employees should be able to calculate their compensation, but the calculation may differ by type
- The system should be able to handle a collection of different employee types polymorphically

**Business Rules and Data Requirements:**

The system must track three types of employees with the following data and compensation rules:

1. **Base Employee (Entry-level/Contractor):**
   - Required data: employee ID, full name, hourly rate ($/hour)
   - Compensation formula: `hourly_rate × 160` (assumes 160 hours/month)
   - Work schedule: Standard 40 hours/week

2. **Full-Time Employee (Salaried):**
   - Inherits from Base Employee
   - Additional data: annual salary, department name
   - Compensation formula: `annual_salary / 12` (monthly salary)
   - Benefits: Receives standard company benefits package
   - Override hourly rate concept with fixed salary

3. **Manager (Senior Leadership):**
   - Inherits from Full-Time Employee
   - Additional data: team size (number of direct reports), bonus percentage (as decimal, e.g., 0.15 for 15%)
   - Compensation formula: `(annual_salary / 12) × (1 + bonus_percentage)` (monthly salary + bonus)
   - Benefits: Same as Full-Time Employee plus bonus compensation
   - Additional responsibility: Must track and report team size

**Specific Requirements:**
- Employee IDs must be stored and retrievable
- All monetary values should be in dollars (float)
- Compensation calculations must return monthly pay amounts
- Each employee type must be able to display their information including their specific attributes
- The system should clearly show the difference between hourly, salaried, and bonus-based compensation

**Design Considerations:**
- How should you structure the inheritance: Base → Full-Time → Manager?
- What attributes are common to all employees (should be in base class)?
- Which compensation calculation should be in the base class, and how should subclasses override it?
- How can Full-Time Employee override the hourly rate concept with salary?
- How can Manager extend the Full-Time Employee's compensation with bonuses?
- How should `super()` be used to avoid duplicating the salary calculation in Manager?
- What information should each employee display, and how should subclasses extend this?

**Example Usage:**
Your implementation should support usage similar to this (exact method names are up to you):

```python
# Create different types of employees
contractor = Employee("E001", "Alice Johnson", 25.0)  # $25/hour
full_timer = FullTimeEmployee("E002", "Bob Smith", 90000, "Engineering")  # $90k/year
manager = Manager("E003", "Carol White", 150000, "Engineering", 8, 0.15)  # $150k/year, 8 reports, 15% bonus

# All employees can display their information
print(contractor.get_info())
# Example output: "Employee E001: Alice Johnson, Hourly Rate: $25.00/hr"

print(full_timer.get_info())
# Example output: "Full-Time Employee E002: Bob Smith, Department: Engineering, Salary: $90,000/year"

print(manager.get_info())
# Example output: "Manager E003: Carol White, Department: Engineering, Salary: $150,000/year, Team Size: 8, Bonus: 15%"

# Calculate monthly compensation (each type uses different formula)
contractor_pay = contractor.calculate_compensation()
print(contractor_pay)    # Output: 4000.0 (25 * 160)

full_timer_pay = full_timer.calculate_compensation()
print(full_timer_pay)    # Output: 7500.0 (90000 / 12)

manager_pay = manager.calculate_compensation()
print(manager_pay)       # Output: 14062.5 (150000/12 * 1.15)

# Demonstrate polymorphism - treat all employees uniformly
employees = [contractor, full_timer, manager]
total_monthly_payroll = sum(emp.calculate_compensation() for emp in employees)
formatted_total = f"${total_monthly_payroll:,.2f}"
print(f"Total monthly payroll: {formatted_total}")
# Output: Total monthly payroll: $25,562.50

# Each employee type can be used through the same interface
for emp in employees:
    emp_info = emp.get_info()
    emp_pay = emp.calculate_compensation()
    formatted_pay = f"${emp_pay:,.2f}"
    print(f"{emp_info} - Monthly Pay: {formatted_pay}")
```

**Testing Requirements:**
- Write at least 5 unit tests that verify:
  - Base Employee compensation calculation (hourly rate × 160 = monthly pay)
  - Full-Time Employee compensation calculation (annual salary ÷ 12 = monthly pay)
  - Manager compensation calculation with bonus ((annual salary ÷ 12) × (1 + bonus percentage) = monthly pay)
  - Polymorphism: All three employee types can be stored in a collection and their compensation calculated uniformly
  - Information display includes all relevant data for each employee type (ID, name, and type-specific fields)

**Constraints:**
- Maximum 3 levels of inheritance (Employee → FullTimeEmployee → Manager)
- Use type hints for all method parameters and return values
- Each class should have a clear, single responsibility
- Use `super()` where appropriate to avoid code duplication

**Note:** While the business requirements and formulas are specified, you must design the class structure, method names, and implementation details yourself.

---


## Exercise 3: Implement Your Own LRU Cache with TTL

**Description:**
Implement a custom Least Recently Used (LRU) Cache class called `MyLruCache` that efficiently manages cached items with both size constraints and time-to-live (TTL) expiration. This exercise will challenge you to design and combine appropriate data structures to achieve optimal performance characteristics.

**Learning Objectives:**
- Understand and implement the LRU (Least Recently Used) cache eviction policy
- Design and combine appropriate data structures to achieve O(1) operations
- Work with time-based expiration (TTL - Time To Live)
- Design a class with multiple interacting components
- Implement efficient cache operations that meet specific performance requirements

**Background:**
An LRU Cache is a data structure that:
- Stores key-value pairs with a maximum capacity (maxsize)
- When the cache is full and a new item is added, it removes the least recently used item
- "Recently used" means either accessed (via get) or added/updated (via set)
- All operations (get and set) must be O(1) - constant time complexity

You'll need to carefully consider which data structures can provide fast lookups, fast insertions/deletions, and maintain ordering information simultaneously.

**Requirements:**

1. **Class Design:**
   - Create a class `MyLruCache` with the following initialization parameters:
     - `maxsize` (int): Maximum number of items the cache can hold (must be > 0)
     - `ttl` (float): Time-to-live in seconds for cached items (must be > 0)

2. **Methods to Implement:**
   - `get(key: str) -> Any | None`:
     - Returns the value associated with the key
     - Returns `None` if the key doesn't exist OR if the item's TTL has expired
     - If the key exists and is not expired, mark it as recently used (move to front)
     - When an item is found to be expired during get, remove it from the cache
   - `set(key: str, value: Any) -> None`:
     - Adds or updates a key-value pair in the cache
     - If the key already exists, update its value and refresh its TTL
     - If adding a new key would exceed maxsize, remove the least recently used item first
     - Mark the newly set item as most recently used
     - Record the current timestamp for TTL tracking
   - `clear() -> None`:
     - Removes all items from the cache
   - `__len__() -> int`:
     - Returns the current number of items in the cache
   - `__contains__(key: str) -> bool`:
     - Returns `True` if the key exists and has not expired, `False` otherwise

3. **Performance Requirements:**
   - Both `get()` and `set()` operations MUST be O(1) average time complexity
   - You must design your data structures to support:
     - Fast lookup by key (O(1))
     - Fast insertion and removal (O(1))
     - Tracking the order of usage (which items are most/least recently used)
     - Tracking timestamps for TTL expiration

4. **Implementation Hints:**
   - Think about what operations you need: lookup by key, track order of access, remove from middle, add to end
   - Consider what data structures provide O(1) operations for different needs
   - You may need to implement your own helper classes or combine multiple data structures
   - Use `time.time()` to track timestamps for TTL expiration checking
   - Consider how to efficiently move items when they're accessed (mark as recently used)
   - Consider how to efficiently find the least recently used item for eviction

5. **Edge Cases to Handle:**
   - Accessing a non-existent key should return `None`
   - Accessing an expired key should return `None` and remove the key from cache
   - Setting a key that already exists should update its value and refresh its TTL
   - When cache is at maxsize and a new key is added, evict the LRU item
   - Clear should work on both empty and non-empty caches

**Example Usage:**

```python
import time

# Create a cache with max 3 items and 2-second TTL
cache = MyLruCache(maxsize=3, ttl=2.0)

# Add some items
cache.set("user:1", {"name": "Alice", "age": 30})
cache.set("user:2", {"name": "Bob", "age": 25})
cache.set("user:3", {"name": "Charlie", "age": 35})

# Get items (O(1) operation)
print(cache.get("user:1"))  # Output: {"name": "Alice", "age": 30}
print(cache.get("user:2"))  # Output: {"name": "Bob", "age": 25}
print(len(cache))           # Output: 3

# Add a 4th item - should evict least recently used (user:3)
cache.set("user:4", {"name": "David", "age": 40})
print(cache.get("user:3"))  # Output: None (was evicted)
print(cache.get("user:4"))  # Output: {"name": "David", "age": 40}
print(len(cache))           # Output: 3

# Test TTL expiration
cache.set("temp", "temporary_data")
print(cache.get("temp"))    # Output: "temporary_data"
time.sleep(2.1)             # Wait for TTL to expire
print(cache.get("temp"))    # Output: None (expired)

# Check if key exists
print("user:1" in cache)    # Output: True
print("user:999" in cache)  # Output: False

# Clear the cache
cache.clear()
print(len(cache))           # Output: 0
```

**Testing Requirements:**
Write comprehensive unit tests using `pytest` that verify:

1. **Basic Operations:**
   - Setting and getting values works correctly
   - Getting a non-existent key returns `None`
   - Updating an existing key updates the value

2. **LRU Eviction:**
   - When maxsize is reached, the least recently used item is evicted
   - Accessing an item (via get) updates its usage and prevents eviction
   - The correct item is evicted in various usage patterns

3. **TTL Expiration:**
   - Items expire after the TTL period
   - Expired items return `None` when accessed
   - Expired items are removed from the cache
   - Setting an existing key refreshes its TTL

4. **Edge Cases:**
   - Cache behavior with maxsize=1
   - Clear operation works correctly
   - `__len__` returns correct count
   - `__contains__` respects TTL expiration

**Constraints:**
- You may NOT use Python's `functools.lru_cache` or any third-party caching libraries
- You MUST design and implement your own solution that achieves O(1) performance
- Both `get()` and `set()` must be O(1) average time complexity
- Use type hints for all method parameters and return values
- The solution must pass all linting requirements (black, flake8, mypy)