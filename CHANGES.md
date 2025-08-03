**Overview**

This document summarizes the critical issues identified in the original app.py, the changes made to refactor the project, and key architectural decisions.

**Major Issues Identified**

    1.Code Structure

        All logic was tightly coupled in a single file (app.py).

        No separation between routing, database operations, and utilities.

    2.Security Vulnerabilities

        SQL queries were directly interpolated, exposing the app to SQL Injection.

        Passwords were stored in plain text without hashing.

        Input validation was missing or improperly handled.

    3.Best Practices Violated

        No error handling or HTTP status codes.

        Used print() for logging.

        json.loads(request.get_data()) used instead of Flask’s request.get_json().

        No model abstraction or centralized database connection.

**Changes Made**

1. Project Restructure:

    Created a modular app structure:

        `app/
        
          ├── __init__.py
        
          ├── routes/user_routes.py
        
          ├── db.py
        
          └── utils.py`

    Moved routing logic to user_routes.py Blueprint.

    Centralized DB connection in db.py.


2. Security Improvements:

    Parameterized all SQL queries to eliminate SQL injection risk.

    Hashed passwords using SHA-256 (utils.py).

    Removed all plaintext password usage.


3. Data Validation & Error Handling:

    Added proper checks for missing fields (e.g., name, email, password).

    Added error messages and appropriate HTTP status codes (400, 401, 404, 201).

    Used Flask’s request.get_json() instead of manually parsing raw data.


4. Response Format:

    Replaced stringified responses (str(user)) with proper JSON responses using jsonify.

    Returned structured success/failure messages in JSON.