# Class Exercises: Server Side Development

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.

---

## Exercise 1: Online Store - Product Management System

**Description:**
Build the foundation for an online store application (Amazon-like) by implementing a complete product management system. You'll create both a service layer for business logic and a REST API layer using FastAPI. This exercise demonstrates the separation of concerns between business logic (service layer) and HTTP handling (API layer).

The exercise is divided into two parts that build on each other:
- **Part 1**: Implement the service layer with JSON file persistence
- **Part 2**: Create the REST API layer using FastAPI

**Learning Objectives:**
- Understand the separation between service layer and API layer
- Implement CRUD operations with persistent storage
- Work with JSON files
- Build RESTful APIs using FastAPI
- Practice proper HTTP status codes and error handling
- Use dataclasses for data modeling
---

### Part 1: Service Layer for Product Management

**Requirements:**

**Product Data Model:**
Create a `Product` dataclass with the following fields:
- `id` (int) - Unique product identifier
- `name` (str) - Product name
- `description` (str) - Product description
- `price` (float) - Product price in dollars
- `stock` (int) - Available quantity in stock

**Service Layer Implementation:**
Create a `ProductsService` class that manages products with the following functionality:

1. **Initialization**:
   - Use the JSON Shay sent

2. **CRUD Operations**:
   - `get_all_products() -> list[Product]` - Return all products
   - `get_product_by_id(product_id: int) -> Optional[Product]` - Get a specific product
   - BONUS: `create_product(name: str, description: str, price: float, stock: int) -> Product` - Create a new product
   

---

### Part 2: REST API for Product Management

**Description:**
Now that you have a working service layer, create a REST API using FastAPI that exposes HTTP endpoints for managing products. The API layer should handle HTTP requests/responses and delegate all business logic to the service layer.

**Requirements:**

1. **API Setup**:
   - Create a new module `products_app.py` for your FastAPI application
   - Import the `ProductsService` and related models from your service module
   - Create a FastAPI app instance with appropriate title, description, and version
   - Create a single instance of `ProductsService` to be used by all endpoints

2. **API Endpoints**:
   Implement the following RESTful endpoints:

   - `GET /products` - Get all products
     - Response: `200 OK` with list of products
     - Response model: `list[Product]`

   - `GET /products/{product_id}` - Get a specific product
     - Response: `200 OK` with the product if found
     - Response: `404 Not Found` if product doesn't exist
     - Response model: `Product`

   - BONUS: `POST /products` - Create a new product
     - Request body: `CreateProductRequest`
     - Response: `201 Created` with the created product
     - Response model: `Product`


**Manual Testing:**
After implementing the API, you can test it manually:

1. Start the server:

2. Visit the automatic API documentation:
   - Swagger UI: http://localhost:8000/docs

3. Use the interactive docs to test your endpoints, or use curl:
   ```bash
   # Create a product
   curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{"name":"Keyboard","description":"Mechanical keyboard","price":89.99,"stock":50}'

   # Get all products
   curl "http://localhost:8000/products"

   # Get specific product
   curl "http://localhost:8000/products/1"

   ```

---