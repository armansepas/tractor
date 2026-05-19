import json
import time
import urllib3
import requests
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CITIES_JSON_PATH = Path(__file__).parent / "cities.json"
API_URL = "https://bck.behtarino.com/api/v1/categories/?city_id={}&format=json"
MAX_CITY_ID = 5000


def extract_city_from_rank_link(rank_page_link: str) -> str | None:
    parts = rank_page_link.strip("/").split("/")
    if len(parts) >= 2:
        return parts[2]
    return None


def load_existing() -> set[str]:
    if CITIES_JSON_PATH.exists():
        with open(CITIES_JSON_PATH, encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_cities(cities: set[str]):
    with open(CITIES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(cities), f, ensure_ascii=False, indent=2)


def main():
    existing = load_existing()
    print(f"Loaded {len(existing)} existing cities.")

    for city_id in range(1, MAX_CITY_ID + 1):
        time.sleep(0.1)
        url = API_URL.format(city_id)
        try:
            resp = requests.get(url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[{city_id}] Error: {e}")
            continue

        categories = data.get("data", [])
        if not categories:
            continue

        added = False
        for cat in categories:
            rank_page = cat.get("rank_page")
            if rank_page is None:
                continue
            link = rank_page.get("rank_page_link")
            if link is None:
                continue
            city = extract_city_from_rank_link(link)
            if city and city not in existing:
                existing.add(city)
                added = True

        if added:
            save_cities(existing)
            print(f"[{city_id}] Added new cities, total: {len(existing)}")

        if city_id % 500 == 0:
            print(f"[{city_id}] Progress... total cities: {len(existing)}")

    print(f"Done. Total cities: {len(existing)}")


if __name__ == "__main__":
    main()
