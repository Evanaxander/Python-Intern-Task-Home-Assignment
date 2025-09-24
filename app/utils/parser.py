from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class ScrapedItem:
    title: str
    url: str
    category: str | None
    price: str | None
    author: str | None


def parse_book_list(html: str) -> list[ScrapedItem]:
    """Parse a books.toscrape.com catalogue page.

    We extract: title, url, category (unknown at list level), price (from listing), author (not on list page; kept None).
    """
    soup = BeautifulSoup(html, "html.parser")
    items: list[ScrapedItem] = []
    for article in soup.select("article.product_pod"):
        a = article.select_one("h3 a")
        if not a:
            continue
        title = a.get("title") or a.text.strip()
        href = a.get("href") or ""
        # Normalize relative links used by the site
        if href and not href.startswith("http"):
            href = href.lstrip("./")
            href = f"https://books.toscrape.com/catalogue/{href}"
        price_el = article.select_one("p.price_color")
        price = price_el.text.strip() if price_el else None
        items.append(ScrapedItem(title=title, url=href, category=None, price=price, author=None))
    return items
