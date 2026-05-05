import requests
from bs4 import BeautifulSoup
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def _get_secret(key: str) -> str:
    """Get secret from Streamlit secrets (cloud) or .env (local)."""
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

SCRAPERAPI_KEY = _get_secret("SCRAPERAPI_KEY")

def get_bestsellers(amazon_url: str) -> list[dict]:
    """
    Scrape Amazon Best Sellers page using ScraperAPI + BeautifulSoup
    """

    # ScraperAPI renders the page and bypasses Amazon's bot protection
    scraper_url = "https://api.scraperapi.com"
    params = {
        "api_key":  SCRAPERAPI_KEY,
        "url":      amazon_url,
        "render":   "true",        # renders JavaScript
        "country_code": "in",      # amazon.in
    }

    print("Fetching page via ScraperAPI...")
    response = requests.get(scraper_url, params=params, timeout=60)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    # Amazon Best Sellers grid items
    items = soup.select("div.zg-grid-general-faceout")

    if not items:
        # fallback selector
        items = soup.select("li.zg-item-immersion")

    print(f"Found {len(items)} raw items")

    for i, item in enumerate(items[:10], start=1):
        try:
            # Title
            title_el = (
                item.select_one("div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y") or
                item.select_one("span.zg-text-center-align") or
                item.select_one("div.p13n-sc-truncate") or
                item.select_one("a.a-link-normal span")
            )
            title = title_el.get_text(strip=True) if title_el else "N/A"

            # Price
            price_el = (
                item.select_one("span.p13n-sc-price") or
                item.select_one("span._cDEzb_p13n-sc-price_3mJ9Z") or
                item.select_one("span.a-color-price")
            )
            price_text = price_el.get_text(strip=True) if price_el else "0"
            price = float(
                price_text.replace("₹", "")
                          .replace(",", "")
                          .replace("$", "")
                          .strip()
                          .split()[0]
            ) if price_text != "0" else 0.0

            # Rating
            rating_el = item.select_one("span.a-icon-alt")
            rating_text = rating_el.get_text(strip=True) if rating_el else "0"
            rating = float(rating_text.split()[0]) if rating_text != "0" else 0.0

            # Review count
            review_el = (
                item.select_one("span.a-size-small") or
                item.select_one("a.a-link-normal span.a-size-small")
            )
            review_text = review_el.get_text(strip=True) if review_el else "0"
            review_count = int(
                review_text.replace(",", "")
                           .replace("(", "")
                           .replace(")", "")
                           .strip()
            ) if review_text.replace(",", "").strip().isdigit() else 0

            # ASIN from link
            link_el = item.select_one("a.a-link-normal")
            link = "https://www.amazon.in" + link_el["href"] if link_el and link_el.get("href") else ""
            asin = ""
            if "/dp/" in link:
                asin = link.split("/dp/")[1].split("/")[0]

            products.append({
                "rank":         i,
                "title":        title,
                "asin":         asin,
                "price":        price,
                "rating":       rating,
                "review_count": review_count,
                "url":          link,
            })

        except Exception as e:
            print(f"Error parsing item {i}: {e}")
            continue

    return products


# ── Test ───────────────────────────────────────────────────
if __name__ == "__main__":
    url = "https://www.amazon.in/gp/bestsellers/beauty/ref=zg_bs_nav_beauty_0"
    products = get_bestsellers(url)

    if products:
        print(f"\n✅ Got {len(products)} products:\n")
        for p in products:
            print(f"  #{p['rank']} | {p['title'][:50]} | ₹{p['price']} | ⭐{p['rating']} | {p['review_count']} reviews")
    else:
        print("❌ No products found")
