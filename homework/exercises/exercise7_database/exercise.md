# SQL Exercise — Building a Food Delivery Platform

## Overview

You've just been hired as a backend developer at **"QuickBite"**, a food delivery startup.  
Your job is to **design the database from scratch**, populate it with realistic data, and write the queries that the business team needs for their daily reports.

---

## Part 1 — Entity Design (Pen & Paper)

Before writing any SQL, you need to understand the business.

### The Business Requirements

QuickBite works like this:

- **Restaurants** sign up to the platform. Each restaurant has a name, address, city, cuisine type (e.g., Italian, Japanese, Burgers), a rating (1–5), and whether they're currently active.
- Each restaurant has a **menu** with items. Each item has a name, description, price, and a category (e.g., Main, Side, Drink, Dessert).
- **Customers** register with their name, email, phone number, city, and registration date.
- Customers place **orders** from a restaurant. Each order has a date/time, a status (`pending`, `preparing`, `delivering`, `delivered`, `cancelled`), and a delivery address.
- Each order contains one or more **order items** — a reference to a menu item and a quantity.
- After an order is delivered, the customer can leave a **review** for the restaurant — a rating (1–5) and an optional text comment.

### Your Task

1. **Identify all the entities** (tables) you'll need.
2. For each entity, list the **columns** and their types.
3. Identify the **relationships** between entities and their types:
   - Which are **one-to-many**?
   - Which are **many-to-many**? (Do you need a relationship table?)
5. Decide where you need **foreign keys**

---

## Part 2 — Create the Database and Tables

Now translate your design into SQL.

### Requirements

- Create a database called `quickbite`.
- Create all tables with proper column types, primary keys, foreign keys, and constraints.
- Use `AUTO_INCREMENT` for IDs.
- Use appropriate data types (`VARCHAR`, `INT`, `DECIMAL`, `TEXT`, `DATETIME`, `ENUM`, `BOOLEAN`).
- Add `NOT NULL` where it makes sense.

---

## Part 3 — Populate with Sample Data

Insert enough data to make the queries interesting. 
Specifically here, and ONLY here, you can use AI to generate the `INSERT INTO` statements. You can also insert manually.

### Tips for Good Test Data

- Make sure at least **one restaurant has no orders**.
- Make sure at least **one customer has never left a review**.
- Include orders from **different months**.
- Include at least **one cancelled order**.
- Have a customer with **many orders** and a customer with **just one**.

---

## Part 4 — Queries

**1.** Select all restaurants sorted by name alphabetically.

**2.** Select all menu items that cost more than ₪40, sorted by price descending.

**3.** Find all restaurants whose name contains "burger" (case-insensitive).

**4.** Select all orders with status `delivered` or `cancelled`.

**5.** Find all menu items in the `Dessert` category, sorted by price ascending.

**6.** Select all customers who registered in 2024.

**7.** Find all restaurants with a rating of 4.0 or higher that are active.

**8.** Show all orders with the customer name and restaurant name.

**9.** For each restaurant, show how many menu items they have. Sort by count descending.

**10.** Show all reviews alongside the customer name and restaurant name.

**11.** For each order, calculate the **total price** (sum of item price × quantity). Show the order ID, customer name, restaurant name, and total.

**12.** Find the **most expensive menu item** for each restaurant. Show restaurant name, item name, and price.

**13.** Show the **number of orders per status** (how many pending, how many delivered, etc.).

**14.** List all customers who have **never placed an order**.

**15.** For each restaurant, show the **average review rating**. Only include restaurants with **3 or more reviews**. Sort by average rating descending.

**16.** Find the **top 3 customers** by total amount spent across all their orders.

**17.** Find customers who have ordered from **more than 3 different restaurants**.

**18.** Write a single query that shows a **"platform dashboard"**:
- Total active restaurants
- Total customers
- Total delivered orders this month
- Total revenue this month
- Average order value this month
- The cuisine type with the highest revenue this month

---

## Tips

- **Run each query after writing it.** Don't write 5 queries and then test — build incrementally.
- **Use aliases** (`AS`) to keep your output readable.
- **When stuck on a hard query**, break it into smaller pieces. Get the inner part working first, then wrap it.
- **You will need to learn** about `HAVING` and `UNION` to write some of the requested queries

Good luck!