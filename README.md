# School Management System (SMS) + Scraper

A compact FastAPI + SQLAlchemy backend with a web scraper that imports data into a relational database. Built to satisfy the assignment requirements.

## Features
- FastAPI + SQLAlchemy (2.0 style) with Pydantic schemas
- Domain OOP classes (Person [abstract], Student, Teacher, Course, Enrollment)
- CRUD endpoints for students, teachers, courses, enrollments
- Business rules: prevent duplicate enrollment, enforce course capacity
- Scraper CLI for books.toscrape.com
  - Respects robots.txt and sets User-Agent
  - Saves JSON to `samples/scraped.json`
  - Optional `--db` flag inserts rows into `scrapedresources` table
- Uses environment variables for DB config
- Pytest tests (rules, API, scraper parsing)

## Quickstart

### 1) Install
```powershell
# From repository root
python -m venv .venv ; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Run API
```powershell
# DB URL can be configured in .env (see .env.example)
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000/docs for interactive docs.

### 3) Scraper CLI
```powershell
# Scrape first 2 pages and save JSON to samples/scraped.json
python scrape.py --pages 2

# Also insert into DB table `scrapedresources`
python scrape.py --pages 2 --db
```

### 4) Run tests
```powershell
pytest -q
```

## Example Endpoints
- POST /students – create student
- GET /students/{id} – fetch student
- POST /courses – create course (with capacity)
- POST /students/{id}/enroll – enroll in course (checks capacity, duplicates)
- POST /import/scraped – import scraped JSON
- GET /scrapedresources – list imported scraped rows

## Project Layout
```
app/
  api/                 # Routers
  utils/               # Helpers (scraper parsing)
  main.py              # FastAPI app
  config.py            # Settings via env vars
  db.py                # Engine and session
  models.py            # SQLAlchemy ORM
  schemas.py           # Pydantic models
  crud.py              # DB services and business rules
samples/
  scraped.json         # Output of scraper
tests/                 # Pytests
scrape.py              # CLI scraper
```

## Notes
- Default DB: SQLite `app.db` in project root. Override with `DATABASE_URL` (e.g., Postgres).
- See DESIGN.md for OOP pillars and architecture overview.
