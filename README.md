# URL Shortener (Midterm Project)

This project implements a robust, high-performance URL shortener service using Python and FastAPI, featuring a layered architecture, PostgreSQL for data persistence, and Alembic for database migrations.

## 🌟 Features

* **Atomic Link Creation:** Generates a unique, short, Base62 encoded code for any long URL.
* **Unique Redirection:** Redirects users from the short code (`/u/{code}`) to the original URL (`HTTP 302 Found`).
* **Full CRUD:** Supports creating, viewing, and deleting shortened URLs.
* **Stable Data Layer:** Uses SQLAlchemy ORM and Alembic migrations for reliable schema management.

## 🛠️ Technologies Used

| Category | Tool / Framework | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Core implementation language. |
| **Web Framework** | FastAPI | High-performance API development. |
| **Database** | PostgreSQL | Robust relational database. |
| **ORM** | SQLAlchemy 2.0 | Python SQL Toolkit and Object Relational Mapper. |
| **Migrations** | Alembic | Database migration management. |
| **Dependency Mgmt** | Poetry | Project packaging and dependency management. |
| **Containerization** | Docker | Running the PostgreSQL database service. |

## 📐 Project Architecture

The application follows a clean, **layered architecture** to separate concerns:

1.  **API Layer (`app/api/`):** Handles HTTP requests, input validation (Pydantic), and returns responses. Uses dependency injection to access the Service layer.
2.  **Service Layer (`app/services/`):** Contains the business logic, such as Base62 encoding, transaction management, and error handling.
3.  **Repository Layer (`app/repositories/`):** Manages all database interaction (CRUD operations), hiding SQLAlchemy details from the Service layer.
4.  **Model Layer (`app/models/`):** Defines the structure of the database tables (e.g., the `URL` model).

## 🚀 Setup and Installation

### 1. Prerequisites

You must have **Docker** (for PostgreSQL) and **Poetry** installed on your system.

### 2. Database Setup

Ensure your `.env` file matches the PostgreSQL container settings, then start the container:

```bash
# Start the PostgreSQL container
docker run --name url-shortener-db -e POSTGRES_USER=shortener_user \
  -e POSTGRES_PASSWORD=shortener_password -e POSTGRES_DB=url_shortener_db \
  -p 5432:5432 -d postgres:16
