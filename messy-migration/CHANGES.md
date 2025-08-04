# CHANGES.md

## 🐛 Major Issues Identified

1. **SQL Injection Vulnerabilities**
   - Direct string interpolation used in SQL queries.
   - Risk of malicious user input compromising the database.

2. **Plaintext Password Storage**
   - User passwords were stored without hashing.
   - Major security flaw, especially for production.

3. **No Input Validation**
   - API accepted any data without checks (e.g., empty email, short passwords, bad formats).

4. **Poor Response Formatting**
   - Responses were returned as raw strings, not proper JSON.
   - No HTTP status codes used.

5. **Monolithic Code Structure**
   - All logic was in one file.
   - Hard to maintain, test, or scale.

6. **Missing Error Handling**
   - API crashes if given invalid JSON or missing keys.
   - No try-except blocks for critical database operations.

---

## ✅ Changes Made and Why

1. **Prevented SQL Injection**
   - Replaced all queries with parameterized ones using `?` placeholders.

2. **Secured Passwords**
   - Used `bcrypt` to hash passwords before storing.
   - Added password comparison logic on login.

3. **Validated Input**
   - Checked for required fields.
   - Added email format validation using regex.
   - Enforced minimum password length.

4. **Consistent JSON Responses**
   - Used `jsonify()` for all responses.
   - Returned appropriate HTTP status codes (e.g., 200, 400, 401, 404, 500).

5. **Restructured Project**
   - Separated concerns:
     - `app.py` → Entry point
     - `routes/user_routes.py` → API endpoints
     - `db.py` → DB connection logic
     - `utils/security.py` → Hashing and validation logic

6. **Improved Error Handling**
   - Wrapped database operations in `try-except`.
   - Returned helpful error messages to the client.

---

## 🧠 Assumptions & Trade-Offs

- Assumed SQLite was sufficient for the scope (no external DB setup).
- No session/auth token added since login was a simple check.
- Did not include logging or environment-based config to keep it minimal.
- Didn’t abstract models into ORM (e.g., SQLAlchemy) to avoid overengineering.

---

## ⏳ What I Would Do with More Time

- Add unit tests using `pytest` or `unittest` for all endpoints.
- Integrate SQLAlchemy ORM for better database management.
- Add JWT-based token authentication.
- Implement pagination for `/users`.
- Use Flask’s `app.config` for environment-based configuration (e.g., dev/prod).
- Improve logging and error reporting with tools like `Sentry`.

---

## 🤖 AI Tools Used

- **ChatGPT (GPT-4o)** by OpenAI
  - Used for guidance on secure password handling, regex for email validation, and project structuring best practices.
  - All AI suggestions were manually reviewed and edited to ensure correctness and alignment with requirements.

---

## ✅ How to Run

```bash
# 1. Install dependencies
pip install flask bcrypt

# 2. Initialize the database
python init_db.py

# 3. Start the app
python app.py
