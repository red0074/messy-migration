
## Overview

This document summarizes the critical issues identified in the original `app.py`, the changes made to refactor the project, and key architectural decisions.

---

## Major Issues Identified

### 1. Code Structure
- All logic was tightly coupled in a single file (`app.py`).
- No separation between routing, database operations, and utilities.

### 2. Security Vulnerabilities
- SQL queries were directly interpolated, exposing the app to SQL Injection.
- Passwords were stored in plain text without hashing.
- Input validation was missing or improperly handled.

### 3. Best Practices Violated
- No error handling or HTTP status codes.
- Used `print()` for logging.
- Used `json.loads(request.get_data())` instead of Flask’s `request.get_json()`.
- No model abstraction or centralized database connection.

---

## Changes Made

### 1. Project Restructure
- Created a modular app structure:\
   app/

   ├── init.py

   ├── routes/user_routes.py

   ├── db.py

   └── utils.py
- Moved routing logic to `user_routes.py` using Flask Blueprint.
- Centralized database connection logic in `db.py`.

### 2. Security Improvements
- Parameterized all SQL queries to eliminate SQL injection risk.
- Hashed passwords using SHA-256 (in `utils.py`).
- Removed all plaintext password usage from the database.

### 3. Data Validation & Error Handling
- Added proper checks for required fields (name, email, password).
- Added meaningful error messages with correct HTTP status codes:
- `400` for bad requests
- `401` for failed login
- `404` for not found
- `201` for successful resource creation
- Replaced manual JSON parsing with `request.get_json()`.

### 4. Response Format
- Replaced all `str(user)` responses with properly structured JSON using `jsonify()`.
- Ensured consistent success and failure messages in JSON format.

---

## Assumptions & Trade-offs

- Chose to continue using SQLite for simplicity, but in a real-world application, a NoSQL solution like MongoDB might be better for scalability and flexibility.
- Did not use an ORM like SQLAlchemy to avoid overengineering, staying close to the original raw SQL setup.
- Assumed basic email validity and uniqueness but did not enforce it in the schema.

---

## What I Would Do With More Time

- Build a simple testing UI (web-based interface) where users can test all API routes visually.
- Integrate form-based frontend for API interaction.
- Implement token-based authentication (e.g., JWT).
- Add email validation and uniqueness enforcement.
- Integrate MongoDB or another scalable NoSQL backend for dynamic schema handling.
- Replace `print()` with proper logging (`logging` module).
- Create test coverage using `pytest` and mock database layers.

---

## AI Usage Disclosure

- **Tool Used:** ChatGPT (OpenAI)
- **Purpose:** Referred to best practices for Flask APIs including secure database access, structure modularization, and password handling.
- The actual implementation, design decisions, and code restructuring were guided by my understanding of REST APIs and refined with assistance from the tool.
