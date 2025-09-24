from app.utils.parser import parse_book_list

SAMPLE_HTML = """
<html><body>
<article class="product_pod">
  <h3><a title="Book 1" href="a-light-in-the-attic_1000/index.html">Book 1</a></h3>
  <p class="price_color">£51.77</p>
</article>
<article class="product_pod">
  <h3><a title="Book 2" href="tipping-the-velvet_999/index.html">Book 2</a></h3>
  <p class="price_color">£53.74</p>
</article>
</body></html>
"""

def test_parse_book_list_extracts_items():
    items = parse_book_list(SAMPLE_HTML)
    assert len(items) == 2
    assert items[0].title == "Book 1"
    assert items[0].price == "£51.77"
    assert items[0].url.startswith("https://books.toscrape.com/catalogue/")
