"""
CSV append utility for wiki-tajrobeh profile data.

Provides functions to append profile data to CSV files with proper
flattening of nested structures.
"""

import csv
import os
from pathlib import Path
from typing import Optional

from getProfileData import ProfileData


DATA_DIR = Path("apps/wiki-tajrobeh/data")
CSV_FILENAME = "profiles.csv"


def _ensure_data_dir() -> Path:
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def _get_csv_path() -> Path:
    """Get the full path to the CSV file."""
    return _ensure_data_dir() / CSV_FILENAME


def _csv_exists() -> bool:
    """Check if the CSV file exists."""
    return _get_csv_path().exists()


def _flatten_categories(categories: list) -> tuple[list[str], list[str]]:
    """Extract category names and slugs from a list of CategoryData."""
    names = [cat.name for cat in categories if hasattr(cat, "name")]
    slugs = [cat.slug for cat in categories if hasattr(cat, "slug")]
    return names, slugs


def _flatten_location(obj: Optional) -> tuple[Optional[str], Optional[str]]:
    """Extract name and slug from a location object (ProvinceData or CityData)."""
    if obj is None:
        return None, None
    name = getattr(obj, "name", None)
    slug = getattr(obj, "slug", None)
    return name, slug


def append_profile_to_csv(profile: ProfileData, csv_path: Optional[Path] = None) -> Path:
    """
    Append a ProfileData object to a CSV file.

    Creates the CSV file with headers if it doesn't exist.
    Flattens nested structures (categories, province, city) into comma-separated values.

    Args:
        profile: The ProfileData object to append.
        csv_path: Optional custom path for the CSV file.

    Returns:
        Path to the CSV file.
    """
    if csv_path is None:
        csv_path = _get_csv_path()

    file_exists = csv_path.exists()

    # Flatten nested structures
    category_names, category_slugs = _flatten_categories(profile.categories)
    province_name, province_slug = _flatten_location(profile.province)
    city_name, city_slug = _flatten_location(profile.city)

    row = {
        "province_name": province_name or "",
        "city_name": city_name or "",
        "category_names": ",".join(category_names) if category_names else "",
        "name": profile.name,
        "phone_numbers": ",".join(profile.phone_numbers) if profile.phone_numbers else "",
        "description": profile.description,
        "lat": profile.lat if profile.lat is not None else "",
        "lng": profile.lng if profile.lng is not None else "",
        "website_url": profile.website_url or "",
        "rate": profile.rate,
        "province_slug": province_slug or "",
        "city_slug": city_slug or "",
        "category_slugs": ",".join(category_slugs) if category_slugs else "",
        "is_verified": profile.is_verified,
        "logo": profile.logo or "",
        "slug": profile.slug,
        "harvested_from_url": profile.harvested_from_url,
    }

    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return csv_path
