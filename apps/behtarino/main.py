"""
Entry point for Behtarino scraping pipeline.

Flow:
1. Scrape listing pages for all (category, city) combinations to collect PDP URLs
2. Save PDP URLs to data/behtarino_data.json
3. Scrape each PDP URL for business data
4. Save business data to data/behtarino_business_data.csv
"""

from listing_scraper import scrape_listings
from pdp import scrape_behtarino_to_csv
import json
import time
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')


def load_json(filename):
    with open(os.path.join(BASE_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)


def step_1_scrape_listings(cities, categories):
    """Scrape all listing pages and save PDP URLs to JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, 'behtarino_data.json')
    scrape_listings(cities, categories, output_path)
    return output_path


def save_listings(data, listings_path):
    """Save listings data to JSON, removing empty categories and cities."""
    for city, categories in list(data.items()):
        if not isinstance(categories, dict):
            continue
        for category, urls in list(categories.items()):
            if not urls:
                del categories[category]
        if not categories:
            del data[city]

    with open(listings_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def step_2_scrape_pdps(listings_path):
    """Read PDP URLs from JSON and scrape each one, removing successfully scraped URLs on the fly."""
    with open(listings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    csv_path = os.path.join(DATA_DIR, 'behtarino_business_data.csv')

    total = 0
    errors = 0

    for city, categories in list(data.items()):
        if not isinstance(categories, dict):
            continue
        for category, urls in list(categories.items()):
            if not isinstance(urls, list):
                continue
            remaining = []
            for url in urls:
                if not isinstance(url, str) or not url.startswith('https://'):
                    continue
                try:
                    time.sleep(0.5)
                    scrape_behtarino_to_csv(url, city, category, csv_path)
                    total += 1
                    # Remove this URL from data and save immediately
                    data[city][category].remove(url)
                    save_listings(data, listings_path)
                except Exception:
                    remaining.append(url)
                    errors += 1
            categories[category] = remaining

    save_listings(data, listings_path)
    print(f"\nDone. Scraped: {total}, Errors: {errors}")


if __name__ == '__main__':
    # cities = load_json('cities.json')
    # categories = load_json('categories.json')
    # listings_path = step_1_scrape_listings(cities, categories)
    listings_path = os.path.join(DATA_DIR, 'behtarino_data.json')
    step_2_scrape_pdps(listings_path)
