import json
import asyncio
from typing import Optional
import httpx
from app.config import settings
from app.utils.parser import parse_book_list
from app.schemas import ScrapedResourceIn
from app.db import SessionLocal
from app.models import Base  # noqa: F401  # ensure models import for create_all side effects
from app.db import engine

ROBOTS_URL = "https://books.toscrape.com/robots.txt"
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

HEADERS = {"User-Agent": settings.user_agent}

async def is_scraping_allowed() -> bool:
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
            resp = await client.get(ROBOTS_URL)
            text = resp.text.lower()
            # simplistic check: disallow scraping if site disallows all
            return "disallow: /" not in text
    except Exception:
        # If robots can't be fetched, be conservative and still proceed for this assignment
        return True

async def fetch_page(client: httpx.AsyncClient, page: int) -> str:
    url = BASE_URL.format(page)
    resp = await client.get(url)
    resp.raise_for_status()
    return resp.text

async def scrape_pages(pages: int) -> list[ScrapedResourceIn]:
    allowed = await is_scraping_allowed()
    if not allowed:
        print("Scraping disallowed by robots.txt")
        return []

    items: list[ScrapedResourceIn] = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as client:
        for p in range(1, pages + 1):
            html = await fetch_page(client, p)
            parsed = parse_book_list(html)
            items.extend([
                ScrapedResourceIn(title=i.title, url=i.url, category=i.category, price=i.price, author=i.author)
                for i in parsed
            ])
    return items

async def main(pages: int, save_json: bool = True, insert_db: bool = False, json_path: str = "samples/scraped.json"):
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    items = await scrape_pages(pages)
    if save_json:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([i.model_dump() for i in items], f, ensure_ascii=False, indent=2)
        print(f"Saved {len(items)} items to {json_path}")

    if insert_db and items:
        from app import crud
        db = SessionLocal()
        try:
            crud.insert_scraped(db, items)
            print(f"Inserted {len(items)} rows into scrapedresources")
        finally:
            db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--db", action="store_true", help="Insert into DB as well")
    args = parser.parse_args()
    asyncio.run(main(args.pages, save_json=True, insert_db=args.db))
