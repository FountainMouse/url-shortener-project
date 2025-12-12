# URL Shortener (Midterm Project)

This project implements a robust, high-performance URL shortener service built with Python and FastAPI, adhering strictly to the professional software development standards, layered architecture principles, and technical requirements set for the Software Engineering Midterm Exam.

## Key Features

- **RESTful API:** Four core API routes implemented with proper HTTP verbs and plural naming conventions.
- **Layered Architecture:** Strict separation of Controller, Service, and Repository layers using **Constructor Injection** for clean, testable, and loosely coupled design.
- **Guaranteed Unique Short Codes:** Uses the **ID to Base62 Conversion** method, ensuring every short code is unique, traceable, and prevents collisions.
- **TTL Bonus Feature:** Implemented Time To Live logic to automatically identify and delete expired links, maximizing data cleanliness.
- **Professional Setup:** Utilizes PostgreSQL via Docker, Alembic for migrations, and Poetry for dependency management.

## Technologies & Dependencies

| Category       | Tool / Framework   | Role in Project                              |
|----------------|--------------------|----------------------------------------------|
| **Language**   | Python 3.11+       | Core programming language                    |
| **Framework**  | FastAPI            | High-performance backend API framework       |
| **Database**Database**   | PostgreSQL         | Relational database used for persistence     |
| **ORM**        | SQLAlchemy 2.0     | Used by the Repository layer                 |
| **Migrations** | Alembic            | Manages database schema evolution            |
| **Environment**| Docker             | Runs PostgreSQL container                    |
| **Testing**    | pytest, httpx      | Dev dependencies for testing                 |

## Setup and Installation

### 1. Prerequisites
Ensure **Docker** and **Poetry** are installed and functioning correctly.

### 2. Database Setup
Start the PostgreSQL container exactly as required:

```bash
docker run --name url-shortener-db \
  -e POSTGRES_USER=shortener_user \
  -e POSTGRES_PASSWORD=shortener_password \
  -e POSTGRES_DB=url_shortener_db \
  -p 5432:5432 -d postgres:16

### 3. Install Dependencies & Migrate
# Install packages using the corrected pyproject.toml
```bash
poetry install

# Activate the virtual environment
```bash
poetry shell

# Apply all database migrations via Alembic
```bash
alembic upgrade head

### 4. Run the Application
```bash
uvicorn main:app --reload

## The API is now accessible at http://localhost:8000.
API Endpoints
The system is defined by four core user stories. All routes comply with RESTful Naming Conventions (plural nouns, using HTTP verbs).

HTTP Method,Route,Description,Responsible Team Member
POST,/urls,"Creates a new short URL, validating the original_url. Returns 201 Created.",Alice
GET,/urls,Retrieves a list of all shortened URLs in the system. Returns 200 OK.,Alice
GET,/u/{code},Redirects the user to the original_url. Returns 302 Found.,Bob
DELETE,/urls/{code},Deletes a short URL record by its code. Returns 200 OK.,Bob
Technical Deep Dive: Short Code Generation
The system uses a highly reliable method for generating the unique short code: ID to Base62 Conversion.
1. The Principle (Guaranteed Uniqueness)
Instead of relying on random string generation, this method leverages the sequential, unique nature of the PostgreSQL Primary Key id.

The record is first inserted (with a temporary code) to retrieve the unique integer id assigned by the database.
This id (Base 10) is then mathematically converted into a Base62 string.
Since the input (id) is guaranteed unique, the output (short_code) is also guaranteed unique.

2. The Base62 Alphabet
The short codes use 62 characters for maximum compactness and readability:

0-9 (10 digits)
a-z (26 lowercase letters)
A-Z (26 uppercase letters)

3. Transactional Integrity
The Base62 encoding (implemented in app/utils.py) is performed within a single database transaction using db.flush() and db.commit() to ensure atomicity. This prevents partial records from existing in the event of an error.
The short_code column is defined with a Unique Index (VARCHAR(10), UNIQUE, INDEXED) to prevent data race conditions during concurrent creation attempts.
Bonus User Story: Time To Live (TTL)
The optional TTL (Time To Live) feature was implemented to automatically clean up old links.
Detail,Implementation
TTL Configuration,Set via the environment variable APP_TTL_MINUTES in the .env file
Expiration Logic,Uses created_at timestamp to check if link age exceeds the configured TTL
Cleanup Command,Encapsulated in app/services/url_service.py → delete_expired_urls() method
Criteria,created_at + TTL < now() (The link is older than the allowed TTL)
Midterm Final Checklist
1. API Test Coverage Table

No,User Story / Feature,Route,Responsible Team Member,Status
1,Create Short Link,POST /urls,Alice,Implemented
2,Redirect to Original URL,GET /u/{code},Bob,Implemented
3,Get All Shortened Links,GET /urls,Alice,Implemented
4,Delete Short Link,DELETE /urls/{code},Bob,Implemented

2. Code Generation Method (Section 6.4)
Check the method you used to generate the short code:

 1. Random Generation
 2. ID to Base62 Conversion
 3. Hash-based Generation

3. Bonus User Story: TTL (Expiration Time) for Shortened Links

TTL Feature Implemented

If checked, fill in the following information:

ENV variable or config key used:APP_TTL_MINUTES=1440 (As defined in .env.example)
Location of TTL Logic (File + Function):app/services/url_service.py to delete_expired_urls()
Command/Scheduler Details: The cleanup logic is run via a scheduled command that calls the service method, using the formula: created_at + TTL < now().

4. Postman Collection (Required)
A Postman Collection has been created and includes all four API routes.
For each route, two screenshots have been added:

Successful response (2xx/3xx)
Error-handled response (4xx)

Screenshots are located in the /postman directory.
