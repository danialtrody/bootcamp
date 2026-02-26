/*==================================================
Part 2 - Create the Database and Tables 
==================================================== */

CREATE TABLE restaurants(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(256) NOT NULL,
	city VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(100),
    rating INT,
    is_active BOOLEAN
);

CREATE TABLE menu(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(8,2),
    category VARCHAR(100),
	restaurant_id  INT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE customers(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(256),
    phone_number VARCHAR(20),
	city VARCHAR(100),
    registration_date DATE
);

CREATE TABLE orders(
	id INT AUTO_INCREMENT PRIMARY KEY,
	time DATETIME,
    status VARCHAR(20),
    delivery_address VARCHAR(256),
	restaurant_id  INT,
    customer_id INT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
	FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items(
	menu_id  INT,
    order_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menu(id),
	FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE customer_review(
	id INT AUTO_INCREMENT PRIMARY KEY,
	rating  INT NOT NULL,
    text_comment TEXT DEFAULT NULL,
    order_id INT,
	customer_id INT,
	FOREIGN KEY (order_id) REFERENCES orders(id),
	FOREIGN KEY (customer_id) REFERENCES customers(id)
);


/*==================================================
Part 3 - Populate with Sample Data (using GPT)
====================================================*/

INSERT INTO restaurants (name, address, city, cuisine_type, rating, is_active) VALUES
('Pizza House', '123 Main St', 'Haifa', 'Italian', 4, TRUE),
('Sushi Star', '45 Sea St', 'Tel Aviv', 'Japanese', 5, TRUE),
('Burger Point', '88 Center St', 'Haifa', 'Fast Food', 3, TRUE);

INSERT INTO menu (name, description, price, category, restaurant_id) VALUES
('Pepperoni Pizza', 'Classic pizza with pepperoni', 55.00, 'Main', 1),
('Margherita Pizza', 'Cheese and tomato', 50.00, 'Main', 1),
('Salmon Sushi', 'Fresh salmon sushi', 40.00, 'Main', 2),
('Cheese Burger', 'Beef burger with cheese', 45.00, 'Main', 3);

INSERT INTO customers (name, email, phone_number, city, registration_date) VALUES
('John Smith', 'john@gmail.com', '0501234567', 'Haifa', '2025-01-10'),
('Sara Cohen', 'sara@gmail.com', '0529876543', 'Tel Aviv', '2025-02-15'),
('David Levy', 'david@gmail.com', '0545552222', 'Haifa', '2024-03-01'),
('Danial Trody', 'Danial@gmail.com', '0545552222', 'Haifa', '202-03-01');

INSERT INTO orders (time, status, delivery_address, restaurant_id, customer_id) VALUES
('2025-01-20 12:30:00', 'delivered', 'Haifa Street 1', 1, 1),
('2025-02-10 18:00:00', 'delivered', 'Tel Aviv Street 2', 2, 2),
('2025-02-25 20:15:00', 'cancelled', 'Haifa Street 3', 1, 2),
('2025-03-05 14:00:00', 'delivered', 'Haifa Street 4', 3, 2),
('2025-03-15 19:00:00', 'delivered', 'Haifa Street 5', 1, 3);

INSERT INTO order_items (menu_id, order_id, quantity) VALUES
(1,1,2),
(2,1,1),
(3,2,3),
(4,4,1),
(1,5,1);

INSERT INTO customer_review (rating, text_comment, order_id, customer_id) VALUES
(5, 'Great food!', 1, 1),
(4, 'Nice sushi', 2, 2),
(3, 'Average', 4, 2);


/*==================================================
Part 4 — Queries
==================================================== */

-- 1. Select all restaurants sorted by name alphabetically.
SELECT * FROM restaurants
ORDER BY name;

-- 2. Select all menu items that cost more than ₪40, sorted by price descending.
SELECT * FROM menu
WHERE price > 40
ORDER BY price DESC;

-- 3. Find all restaurants whose name contains "burger" (case-insensitive).
SELECT * FROM restaurants
WHERE name LIKE '%burger%';

-- 4. Select all orders with status delivered or cancelled.
SELECT * FROM orders
WHERE status in ('cancelled','delivered');

-- 5. Find all menu items in the Dessert category, sorted by price ascending.
SELECT * FROM menu
WHERE category = 'Dessert'
order by price ASC;

-- 6. Select all customers who registered in 2024.
SELECT * FROM customers
WHERE registration_date LIKE '%2024%';

-- 7. Find all restaurants with a rating of 4.0 or higher that are active.
SELECT * FROM restaurants
WHERE rating >= 4 and is_active = 1;

-- 8. Show all orders with the customer name and restaurant name.
SELECT customers.name AS 'customer name' , restaurants.name AS 'restaurant name' , orders.* FROM orders
JOIN restaurants ON orders.restaurant_id = restaurants.id
JOIN customers ON orders.customer_id = customers.id;

-- 9. For each restaurant, show how many menu items they have. Sort by count descending.
SELECT restaurants.name, COUNT(menu.restaurant_id) AS 'items'
FROM menu
JOIN restaurants ON menu.restaurant_id = restaurants.id
GROUP BY restaurant_id
ORDER BY items DESC;

-- 10. Show all reviews alongside the customer name and restaurant name.
SELECT restaurants.name AS 'restaurant name' ,
customers.name AS 'customre name', 
customer_review.rating, customer_review.text_comment FROM customer_review
JOIN customers ON customer_id = customers.id
JOIN orders ON order_id = orders.id
join restaurants  ON orders.restaurant_id = restaurants.id;

-- 11. For each order, calculate the total price (sum of item price × quantity). Show the order ID, customer name, restaurant name, and total.
SELECT orders.id AS 'order id' ,
customers.name AS 'customre name',
restaurants.name AS 'restaurants name' ,
SUM(menu.price * order_items.quantity) AS 'total'
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN restaurants ON orders.restaurant_id = restaurants.id
JOIN order_items ON order_items.order_id = orders.id 
JOIN menu ON order_items.menu_id = menu.id
GROUP BY orders.id, customers.name, restaurants.name;

-- 12. Find the most expensive menu item for each restaurant. Show restaurant name, item name, and price.
SELECT restaurants.name AS 'restaurant name',
menu.name AS 'item name',
menu.price AS 'max price'
FROM menu
JOIN restaurants ON menu.restaurant_id = restaurants.id
WHERE menu.price = (
	SELECT MAX(price)
    FROM menu
    WHERE restaurant_id = restaurants.id
);

-- 13. Show the number of orders per status (how many pending, how many delivered, etc.).
SELECT status, COUNT(*) AS 'orders per status' FROM orders
GROUP BY status;

-- 14. List all customers who have never placed an order.
SELECT * FROM customers
LEFT JOIN orders ON orders.customer_id = customers.id
WHERE orders.id IS NULL;

-- 15. For each restaurant, show the average review rating. Only include restaurants with 3 or more reviews. Sort by average rating descending.
SELECT restaurants.id, restaurants.name,
AVG(customer_review.rating) AS average_rating,
COUNT(customer_review.id) AS 'review count'
FROM restaurants
JOIN orders ON orders.restaurant_id = restaurants.id
JOIN customer_review ON customer_review.order_id = orders.id
GROUP BY restaurants.id, restaurants.name
HAVING COUNT(customer_review.id) >= 3
ORDER BY average_rating DESC;

-- 16. Find the top 3 customers by total amount spent across all their orders.
SELECT customers.name , SUM(menu.price) as total_spent
FROM order_items
JOIN menu ON order_items.menu_id = menu.id
JOIN orders ON order_items.order_id = orders.id
JOIN customers ON orders.customer_id = customers.id
GROUP BY  customers.name
ORDER BY total_spent DESC
LIMIT 3;

-- 17. Find customers who have ordered from more than 3 different restaurants.
SELECT customers.name AS 'customer name', COUNT(DISTINCT restaurants.id) AS 'restaurant count'
FROM orders
JOIN restaurants ON orders.restaurant_id = restaurants.id
JOIN customers ON orders.customer_id = customers.id
GROUP BY customers.name
HAVING COUNT(DISTINCT restaurants.id) > 3;

/*
18. Write a single query that shows a "platform dashboard":
Total active restaurants
Total customers
Total delivered orders this month
Total revenue this month
Average order value this month
The cuisine type with the highest revenue this month
*/



