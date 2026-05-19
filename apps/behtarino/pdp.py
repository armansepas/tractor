"""
Scrape individual Behtarino PDP (business detail) pages.
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import os


def scrape_behtarino_business_data(url, city, category):
    """
    Scrape business data from a Behtarino business page.

    Returns:
        dict: Extracted business data, or None if failed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', {'type': 'application/ld+json'})

        if not script_tag:
            print("No JSON-LD script found")
            return None

        json_data = json.loads(script_tag.string)
        telephone = json_data.get('telephone')

        business_data = {
            'city': city,
            'category': category,
            'name': json_data.get('name'),
            'description': json_data.get('description'),
            'telephone': str(telephone) if telephone is not None else None,
            'url': json_data.get('url'),
            'images': json_data.get('image', []),
            'identifier': json_data.get('identifier'),
            'street_address': json_data.get('address', {}).get('streetAddress'),
            'latitude': json_data.get('geo', {}).get('latitude'),
            'longitude': json_data.get('geo', {}).get('longitude'),
            'social_links': json_data.get('sameAs', []),
            'logo': json_data.get('logo'),
            'address_region': json_data.get('address', {}).get('addressRegion'),
            'address_country': json_data.get('address', {}).get('addressCountry'),
            'address_locality': json_data.get('address', {}).get('addressLocality'),
            'rating_value': json_data.get('aggregateRating', {}).get('ratingValue'),
            'rating_count': json_data.get('aggregateRating', {}).get('reviewCount'),
            'worst_rating': json_data.get('aggregateRating', {}).get('worstRating'),
            'best_rating': json_data.get('aggregateRating', {}).get('bestRating'),
            'business_type': json_data.get('@type'),
            'context': json_data.get('@context'),
            'business_id': json_data.get('@id')
        }

        return business_data

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def scrape_behtarino_to_csv(url, city, category, filename=None):
    """
    Scrape business data and append to CSV.

    Args:
        filename: Full path to CSV. Defaults to data/behtarino_business_data.csv
    """
    if filename is None:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, 'behtarino_business_data.csv')

    data = scrape_behtarino_business_data(url, city, category)

    if data:
        df = pd.DataFrame([data])
        file_exists = os.path.isfile(filename)
        df.to_csv(filename, mode='a', index=False, encoding='utf-8', header=not file_exists)
        print(f"Data successfully appended to {filename}")
        return True
    else:
        print("Failed to scrape data")
        return False
