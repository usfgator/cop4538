Purpose
-------
This file guides AI coding agents working on this repo: a small Flask-based contact manager used for CS course exercises. Focus on concrete, repo-specific patterns, dev commands, and places students will modify.

**Big Picture**
- **App type:** Single Flask app (`app.py`) that renders `templates/index.html` and exposes two main routes: `/` (GET) and `/add` (POST).
- **Phases:** Early phases use an in-memory Python list `contacts` (top of `app.py`). Later phases expect DB connectivity: Postgres and MSSQL placeholders exist (`get_postgres_connection`, `get_mssql_connection`).
- **Runtime:** App runs on `0.0.0.0:5000` when started with `python app.py`. Docker setup mirrors local dev via `docker-compose.yml`.

**Key Files / Places to Edit**
- `app.py`: main logic, routes, and the `contacts` data structure students will replace with other DS or DB code.
- `templates/index.html`: Jinja2 template for the UI and form (`name`, `email`).
- `Dockerfile` and `docker-compose.yml`: containerized dev environment; `docker-compose.yml` mounts the repo into `/app` so code changes are live.
- `requirements.txt`: `flask`, `psycopg2-binary`, `pyodbc` — DB drivers expected in later phases.

**Concrete Workflows & Commands**
- Local dev: `pip install -r requirements.txt` then `python app.py` (listens on port 5000).
- Docker: `docker-compose up --build` (exposes ports 5000, 5432, 1433). Note: `docker-compose.yml` mounts `.:/app` for live sync.
- Build image manually: `docker build -t contact-app .` then `docker run -p 5000:5000 contact-app`.

**Project-Specific Conventions**
- Students should implement data-structure changes in the same module-level variables used by `index()` and `add_contact()` to keep template code unchanged.
- Preserve the POST form field names `name` and `email` used in `templates/index.html` when refactoring insertion logic.
- Keep route signatures the same — UI and tests (if added) assume `/` and `/add` behavior.

**Integration Points & Notes**
- Postgres: `postgres_db` (docker-compose) at port `5432`; credentials in `docker-compose.yml` (`student` / `password123` / `contact_db`).
- MSSQL: `mssql_db` at port `1433`; `MSSQL_SA_PASSWORD` is set in compose. Dockerfile installs `msodbcsql17` for `pyodbc`.
- DB drivers are listed in `requirements.txt` — avoid changing versions without testing the Docker build.

**Examples (What to change for common tasks)**
- Replace list append (in `add_contact`) with insertion into another DS or DB:
```
# current
contacts.append({'name': name, 'email': email})

# replace with (example): linked_list.insert(name, email)
```
- When adding DB code, implement and call `get_postgres_connection()` or `get_mssql_connection()`; keep connection logic isolated to those helpers.

**Agent Behavior Guidelines**
- Make minimal, focused edits: prefer small diffs to `app.py` and preserve form and route contracts.
- When adding dependencies, update `requirements.txt` and ensure `Dockerfile` still builds (the Dockerfile runs `pip install -r requirements.txt`).
- If changing runtime behavior, update this file with the exact commands you used to verify (so future agents can reproduce).

If anything here is unclear or you'd like additional examples (e.g., sample LinkedList implementation integrated into `app.py`), tell me which part to expand.
