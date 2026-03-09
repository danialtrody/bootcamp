# CodeValue School - Database Demo

## Project Overview

Throughout the next modules we will build a management system for **CodeValue School of Tech** — a fictional tech bootcamp that manages students, teachers, courses, and enrollments.

This demo focuses on connecting a FastAPI application to a **MySQL** database using **SQLAlchemy** and managing schema changes with **Alembic**. The application follows a three-layer architecture: **routers → services → repositories**.

## Data Model

**Student**

| Field        | Type      | Notes                             |
|--------------|-----------|-----------------------------------|
| student_id   | Integer   | Primary key, auto-generated       |
| first_name   | String    | Required                          |
| last_name    | String    | Required                          |
| email        | String    | Required, unique                  |
| birth_date   | Date      | Optional                          |
| created_at   | DateTime  | Auto-generated (server default)   |

## API Endpoints

**Student Management**

- `GET /students/` — List all students
- `GET /students/{student_id}` — Get a student by ID
- `POST /students/` — Create a new student
- `PUT /students/{student_id}` — Update a student
- `DELETE /students/{student_id}` — Delete a student

## Project Architecture

```
src/
├── secrets_accessor.py      # Loads secrets from .env files
├── database.py              # SQLAlchemy engine, session, and Base
├── app.py                   # FastAPI app with all routers
├── models/
│   └── student.py           # SQLAlchemy ORM model
├── repositories/
│   └── student_repository.py  # Database queries (data layer)
├── services/
│   └── student_service.py     # Business logic (service layer)
├── routers/
│   └── students.py            # HTTP endpoints (presentation layer)
└── tests/
    ├── conftest.py            # Test fixtures and database setup
    ├── fixtures/
    │   └── mock_students.json # Seed data for integration tests
    └── integration_tests/
        └── test_students.py   # Integration tests for the Student API
```

## Getting Started

This project requires a **local MySQL server** running on port `3306`. Make sure MySQL is installed and running on your machine before starting.

1. Make sure your local MySQL server is running on port `3306`
2. Copy `.env_sample` to `.env` and update values if needed
3. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### Exercise 1: Database Connection

#### 1.1 — Create the MySQL user and database

Use your MySQL client (e.g., MySQL Workbench or the CLI) to connect as `root` and run:

```sql
CREATE USER IF NOT EXISTS 'dev'@'%' IDENTIFIED BY 'mysql123';
GRANT ALL PRIVILEGES ON *.* TO 'dev'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

```sql
CREATE DATABASE IF NOT EXISTS school_db;
```

#### 1.2 — Start the server (smoke test)

Run the app and make sure it starts:

```bash
python main.py
```

Make a GET request to `/health` — you should get `{"status": "OK"}`.

#### 1.4 — Explore the existing code

Look at the files that are already implemented for you:

- `src/models/student.py` — the SQLAlchemy `Student` model
- `src/repositories/student_repository.py` — database queries using sessions
- `src/services/student_service.py` — business logic layer
- `src/routers/students.py` — FastAPI endpoints
 
### Exercise 2: Apply Alembic Migrations

```bash
alembic upgrade head
```

#### 2.5 — Test the Student endpoints

Restart the server and test the CRUD endpoints using the Swagger UI at `http://127.0.0.1:8000/docs`.

Insert a student via `POST /students/`, then retrieve, update, and delete it.

#### 3

1. Add to student repository the following methods:
  - find_by_email(email: str) -> Student
     stmt = select(Student).where(Student.email == email)
     return session.scalars(stmt).first()

  - find_by_last_name(last_name: str) -> list[Student]
    stmt = select(Student).where(Student.last_name == last_name)
    return session.scalars(stmt).all()

  - find_by_partial_name(partial_name: str) -> list[Student] # LIKE
    stmt = select(Student).where(Student.first_name.like(f"%{partial_name}%"))
    return session.scalars(stmt).all()

  - update_email(student: Student, new_email: str)
    
    student_to_update = session.get(Student, student.id)
    student_to_update.email = new_email    
    session.commit()

  - delete_student(student: Student)

    student_to_delete = session.get(Student, student.id)
    session.delete(student_to_delete) 
    session.commit()


#### 4 - SQLALCHEMY

1. Fetch all columns for every student and print their first_name.
2. Find the single student who has the email 'test@example.com'.
3. Get a list of all students, sorted by their last_name in alphabetical order.
4. Find all students whose email addresses end with @gmail.com.
5. Find all students who were born before January 1, 2005.
6. Fetch only the 5 most recently created students.
7. Skip the first 10 students and fetch the next 10, ordered by their student_id.
8. Calculate the total number of students currently in the table.
9. Find all students whose first_name starts with "J" AND whose birth_date is not null.
10. Find all students who were born in the month of March, regardless of the year.