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

## ✅ How to Run Messy-migration

```bash
cd messy-migration
# 1. Install dependencies
pip install -r requirements.txt

pip install flask bcry

# 2. Initialize the database
python init_db.py

# 3. Start the app
python app.py


#  URL Shortener Assignment

## ✅ Major Issues Handled

1. **No Core Functionality Implemented**
   - Original `main.py` only had health check routes.
   - All required endpoints (shorten, redirect, analytics) were missing.

2. **Missing Data Layer**
   - `models.py` was empty.
   - No mechanism to store short codes, click counts, or metadata.

3. **No URL Validation**
   - Invalid or malformed URLs could be submitted without error.

4. **No Tests for Core Logic**
   - Only one basic test (`/`) existed.
   - No tests for shorten/redirect/stats.

---

## ✅ Changes Made

### 📁 Project Structure
```bash
url-shortener/
│
├── app/
│ ├── init.py
│ ├── main.py # All routes defined here
│ ├── models.py # In-memory DB (dictionary)
│ ├── utils.py # Short code generation & URL validation
│
├── tests/
│ └── test_main.py # 5 complete test cases using pytest
│
├── requirements.txt # Flask & Pytest
└── README.md # Setup & Usage (if included)
```
---

### 🔨 Implemented Features

#### `POST /api/shorten`
- Validates URL format
- Generates a 6-character alphanumeric short code
- Stores URL with timestamp and click count in memory
- Returns short code + short URL

#### `GET /<short_code>`
- Redirects to original URL
- Increments click count

#### `GET /api/stats/<short_code>`
- Returns click count, original URL, and creation timestamp

---

### 🔒 Validation & Safety
- Invalid or empty URLs are rejected with `400 Bad Request`
- Nonexistent short codes return `404 Not Found`
- Short code collision is prevented by retrying generation

---

### 🧪 Test Coverage

Added 5 Pytest-based tests:
1. Health check
2. Shorten a valid URL
3. Redirect from short URL
4. Stats endpoint tracking clicks
5. Invalid URL rejection

---

## 🧠 Assumptions & Trade-offs

- Used **in-memory dictionary** (`url_store`) as specified.  
  ⚠️ Data will be lost on restart — no persistence added.
- Did not implement user authentication or rate limiting as per the spec.
- Short codes are **random**, no user customization.

---

## ⏳ What I Would Do With More Time

- Store data in a persistent database (e.g., SQLite, Redis)
- Add expiry for short links (TTL support)
- Track per-day click analytics
- Rate limiting or abuse prevention
- Deploy with Docker & write CI tests

---

## 🤖 AI Usage

- **Tool Used**: ChatGPT (GPT-4o) by OpenAI
- **Used for**:
  - Clarifying assignment scope and structure
  - Reviewing Python syntax for Flask, random generation
  - Suggesting test cases
- **Manual Review**: All AI-generated code was reviewed and adapted.

---

## ✅ How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m flask --app app.main run

# Run all tests
pytest


# Shorten URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Get Stats
curl http://localhost:5000/api/stats/<short_code>


