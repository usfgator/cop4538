Purpose
-------
This file guides AI coding agents working on this repo: a small Flask-based contact manager used for CS course exercises. Focus on concrete, repo-specific patterns, dev commands, and places students will modify.

## Big Picture

**App Type:** Single Flask app that renders `templates/index.html` and exposes two main routes: `/` (GET) and `/add` (POST).

**Architecture:**
- **Phase 1 (current):** In-memory Python list `contacts` at module level in `app.py`
- **Phases 2+:** Students will replace the list with custom data structures (LinkedList, Tree) and later with DB backends (Postgres/MSSQL)
- **Runtime:** `python app.py` → Flask on `0.0.0.0:5000` with auto-reload in debug mode
- **Containerized:** `docker-compose.yml` orchestrates Flask app + Postgres + MSSQL with live code sync via volume mount

**Data Flow:**
1. User adds contact via form (`name`, `email`) → POST `/add`
2. `add_contact()` stores in `contacts` list → redirects to `/`
3. `index()` retrieves from `contacts` → renders Jinja2 template with contact cards
4. Template displays contact count implicitly via loop; elapsed time shown in header

## Key Files & Edit Points

| File | Purpose | Student Modifications |
|------|---------|----------------------|
| `app.py` | Main Flask routes & data structures | Replace `contacts` list append logic; implement DB functions |
| `templates/index.html` | Jinja2 UI; contact form & display | Keep `name` and `email` form field names unchanged |
| `requirements.txt` | Python dependencies | Add packages for custom DS or ORM if needed |
| `Dockerfile` | Container image build | System deps installed automatically for MSSQL (`msodbcsql17`) |
| `docker-compose.yml` | Multi-service orchestration | Database credentials baked in; ports exposed for testing |
| `benchmark.py` | Performance measurement template | Students extend for timing DS operations |

## Concrete Workflows & Commands

**Local Development:**
```bash
# First time setup
pip install -r requirements.txt

# Run the app (debug mode, auto-reload on code changes)
python app.py

# Access UI
# http://localhost:5000
```

**Docker Development:**
```bash
# Build and start all services (Flask, Postgres, MSSQL)
docker-compose up --build

# Bring down services
docker-compose down

# View Flask app logs
docker-compose logs web

# The .:/app mount means edits to app.py are live without rebuilding
```

**Database Testing (inside Docker or with local tools):**
- **Postgres:** Connect to `localhost:5432` with user `student` / password `password123` / db `contact_db`
- **MSSQL:** Connect to `localhost:1433` with SA user / password `Password123!`

## Project-Specific Conventions

**Data Structure Integration:**
- Keep `contacts` as a module-level variable in `app.py` (not a class instance) so template renders unchanged
- `add_contact()` must accept form-submitted `name` and `email` fields
- `index()` must return a list-like object with dict items `{'name': '...', 'email': '...'}`

**Route Contracts (Do Not Break):**
- `GET /` → returns rendered `index.html` with title and elapsed_time
- `POST /add` → accepts `name` and `email` form fields, redirects to `/`

**Flask Configuration:**
- `FLASK_TITLE` set at module level; used to personalize the page header
- `elapsed_time` calculated from module-level `start_time` to track app uptime

**Dependency Changes:**
- Modify `requirements.txt` with specific versions (tested with Flask 3.0.0, psycopg2 2.9.9, pyodbc 5.0.1)
- Dockerfile auto-installs from `requirements.txt` and handles MSSQL system packages

## Integration Points & Notes

**Postgres Setup (for later phases):**
- Service: `postgres_db` in `docker-compose.yml`, port 5432
- Credentials: user `student` / password `password123` / database `contact_db`
- Implement `get_postgres_connection()` to return a connection handle (psycopg2)
- Example: `import psycopg2; psycopg2.connect(host='postgres_db', user='student', password='password123', database='contact_db')`

**MSSQL Setup (for later phases):**
- Service: `mssql_db` in `docker-compose.yml`, port 1433
- Credentials: SA user / password `Password123!`
- Implement `get_mssql_connection()` to return a connection handle (pyodbc)
- Dockerfile installs `msodbcsql17` driver; note strong password requirement
- Example: `import pyodbc; pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=mssql_db;UID=sa;PWD=Password123!')`

## Common Refactoring Patterns

**Replace List with LinkedList (example):**
```python
# Current (Phase 1)
contacts.append({'name': name, 'email': email})

# Refactored (Phase 2 - with custom LinkedList class in same file)
from linked_list import LinkedList
contacts = LinkedList()
# In add_contact():
contacts.insert({'name': name, 'email': email})
```

**Migrate to Postgres (example):**
```python
# Replace module-level contacts list:
def get_contacts():
    conn = get_postgres_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, email FROM contacts')
    return [{'name': row[0], 'email': row[1]} for row in cur.fetchall()]

# In index(): pass get_contacts() instead of global contacts
# In add_contact(): execute INSERT instead of append
```

## Agent Behavior Guidelines

- **Make minimal, focused edits:** Prefer small diffs to `app.py` to avoid merge conflicts with student code
- **Preserve form contracts:** Do not rename `name` or `email` form fields; they are tested externally
- **Test Docker builds:** When adding dependencies, verify `docker build -t contact-app .` completes without errors
- **Keep route signatures stable:** Tests and UI assume `/` and `/add` endpoints with current signatures
- **Isolate DB logic:** Put connection code in the `get_postgres_connection()` and `get_mssql_connection()` placeholders to keep routes clean
- **Document changes:** If modifying runtime behavior (e.g., env vars), update this file with the exact commands used to verify

## Verification Checklist

After making changes:
1. **Local:** `python app.py` → form accepts name/email → contact appears in list
2. **Docker:** `docker-compose up --build` → same behavior, ports 5000, 5432, 1433 accessible
3. **Dependencies:** No version conflicts in `requirements.txt`; `Dockerfile pip install` succeeds
4. **Template:** Contact names render without errors; elapsed_time displays correctly

---

If you need to expand any section or see examples for specific phases (LinkedList implementation, DB schema design, ORM migration), contact the maintainer.
