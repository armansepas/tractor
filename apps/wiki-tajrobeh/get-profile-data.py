"""
Fetch profile data from tajrobe.wiki API.

This module provides functionality to retrieve and parse profile data
from the tajrobe.wiki API for a given slug.
"""

from dataclasses import dataclass
from typing import Optional
import requests


@dataclass
class CategoryData:
    """Represents a category extracted from the profile."""
    name: str
    slug: str


@dataclass
class ProvinceData:
    """Represents province information from the profile."""
    name: str
    slug: str


@dataclass
class CityData:
    """Represents city information from the profile."""
    name: str
    slug: str


@dataclass
class ProfileData:
    """Represents the extracted profile data."""
    name: str
    rate: float
    phone_numbers: list[str]
    description: str
    lat: Optional[float]
    lng: Optional[float]
    website_url: Optional[str]
    categories: list[CategoryData]
    province: Optional[ProvinceData]
    city: Optional[CityData]
    is_verified: bool
    logo: Optional[str]
    slug: str
    harvested_from_url: str


def _parse_location(location_value: str) -> tuple[Optional[float], Optional[float]]:
    """Parse location string into lat and lng coordinates."""
    if not location_value:
        return None, None
    try:
        parts = location_value.split(",")
        if len(parts) == 2:
            return float(parts[0].strip()), float(parts[1].strip())
    except (ValueError, IndexError):
        pass
    return None, None


def _extract_attributes(attributes: list[dict]) -> tuple[list[str], Optional[float], Optional[float], Optional[str]]:
    """Extract phone numbers, location, and website from attributes."""
    phone_numbers: list[str] = []
    lat: Optional[float] = None
    lng: Optional[float] = None
    website_url: Optional[str] = None
    
    for attr in attributes:
        key = attr.get("key", "")
        value = attr.get("value", "")
        
        if key == "tel" and value:
            phone_numbers.append(value)
        elif key == "location" and value:
            lat, lng = _parse_location(value)
        elif key == "website" and value:
            website_url = value
    
    return phone_numbers, lat, lng, website_url


def get_profile_data(slug: str, base_url: str = "https://tajrobe.wiki/api/client/profile") -> ProfileData:
    """
    Fetch and parse profile data from tajrobe.wiki API.
    
    Args:
        slug: The profile slug identifier.
        base_url: Base URL for the API endpoint.
    
    Returns:
        ProfileData object containing the extracted profile information.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    url = f"{base_url}/{slug}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WikiTajrobeHarvester/1.0)",
        "Accept": "application/json",
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    
    # Handle API response structure
    if isinstance(data, dict):
        data = data.get("data", data)
    
    # Extract categories
    categories = [
        CategoryData(
            name=cat.get("name", ""),
            slug=cat.get("slug", "")
        )
        for cat in data.get("categories", [])
    ]
    
    # Extract province
    province_data = data.get("province")
    province = None
    if province_data:
        province = ProvinceData(
            name=province_data.get("name", ""),
            slug=province_data.get("slug", "")
        )
    
    # Extract city
    city_data = data.get("city")
    city = None
    if city_data:
        city = CityData(
            name=city_data.get("name", ""),
            slug=city_data.get("slug", "")
        )
    
    # Extract attributes for phone, location, and website
    phone_numbers, lat, lng, website_url = _extract_attributes(data.get("attributes", []))
    
    # Use url from main data if not found in attributes
    if not website_url:
        website_url = data.get("url")
    
    return ProfileData(
        name=data.get("name", ""),
        rate=data.get("rating", 0.0),
        phone_numbers=phone_numbers,
        description=data.get("description", ""),
        lat=lat,
        lng=lng,
        website_url=website_url,
        categories=categories,
        province=province,
        city=city,
        is_verified=data.get("is_verified", False),
        logo=data.get("logo"),
        slug=data.get("slug", slug),
        harvested_from_url=url,
    )
