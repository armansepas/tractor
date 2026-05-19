"""
Scrape Behtarino listing pages for all (category, city) combinations
to collect PDP URLs. Saves results as a nested JSON:
    { city: { category: [url, ...] } }
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import time


def load_or_create_output(output_path):
    """Load existing output JSON or return empty dict."""
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_output(output_path, data):
    """Save nested dict to JSON."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def scrape_listings(cities, categories, output_path):
    seen_urls = set()
    city_services_dict = load_or_create_output(output_path)

    # Collect already-seen URLs from existing data
    for city_cats in city_services_dict.values():
        for urls in city_cats.values():
            for url in urls:
                seen_urls.add(url)

    for service in categories:
        for city in cities:
            urls_list = []
            for page in range(1, 201):
                service_encoded = quote(service)
                city_encoded = quote(city)
                print(f"extracting Service: {service_encoded}, in city:{city_encoded} page:{page}")
                url = f"https://behtarino.com/r/{service_encoded}/{city_encoded}?page={page}"

                try:
                    res = requests.get(url, timeout=10)
                    res.raise_for_status()
                except:
                    break

                soup = BeautifulSoup(res.text, 'html.parser')
                script_tag = soup.find('script', type='application/ld+json')
                if not script_tag:
                    break

                try:
                    data = json.loads(script_tag.string)
                    if ('mainEntity' in data and 'itemListElement' in data['mainEntity']
                            and data['mainEntity']['itemListElement']):
                        for business in data['mainEntity']['itemListElement']:
                            url_val = business.get('item', {}).get('url')
                            if url_val and url_val not in seen_urls:
                                seen_urls.add(url_val)
                                urls_list.append(url_val)
                    else:
                        break
                except:
                    continue

                time.sleep(0.5)

            if urls_list:
                if city not in city_services_dict:
                    city_services_dict[city] = {}
                city_services_dict[city][service] = urls_list
                save_output(output_path, city_services_dict)
                print(f"Saved {len(urls_list)} URLs for {city}/{service}")

    print(f"Saved listing URLs to {output_path}")
    return city_services_dict
