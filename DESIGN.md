# Design and OOP Pillars

This project demonstrates the four OOP pillars through a small domain layer and persists via SQLAlchemy.

## OOP Pillars
- Abstraction: `Person` is an abstract concept exposing a `get_display_name()` interface. Concrete classes `Student` and `Teacher` implement it.
- Encapsulation: Domain objects keep their state private and provide behavior (e.g., `Course.enroll()` guards rules). The FastAPI layer does not manipulate SQL rows directly; it calls service functions.
- Inheritance: `Student` and `Teacher` inherit from `Person`.
- Polymorphism: `get_display_name()` behaves differently for `Student` vs `Teacher`.

## Business Rules
- Duplicate enrollment is prevented by a unique constraint and checked in the service.
- Capacity enforced by counting current enrollments before inserting a new one.

## Data Flow
1. Request hits endpoint -> router -> service in `crud.py`.
2. Service validates rules and persists using SQLAlchemy ORM models.
3. Responses serialized via Pydantic schemas.

## Scraper
- Fetches `books.toscrape.com` pages with a custom User-Agent and a minimal robots.txt check.
- Parses HTML with BeautifulSoup in `app/utils/parser.py`.
- Saves JSON to `samples/scraped.json` and can insert into the DB.
