"""
Main harvesting script for wiki-tajrobeh profile data.

Iterates through pages 1-4115, fetches profile hashes, retrieves profile data,
and appends results to a CSV file.
"""

import time
from typing import Optional

from findAllProfiles import find_all_profiles
from getProfileData import get_profile_data, ProfileData
from append import append_profile_to_csv

# Constants
FIRST_PAGE = 1
LAST_PAGE = 4115
REQUEST_DELAY_SECONDS = 0.1  # Rate limiting delay between requests


def _safe_get_profile(hash_value: str, retries: int = 3) -> Optional[ProfileData]:
    """Get profile data with retry logic for transient failures."""
    for attempt in range(retries):
        try:
            return get_profile_data(hash_value)
        except Exception:
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY_SECONDS)
            continue
    return None


def run_harvest() -> None:
    """Execute the full harvesting workflow from page 1 to 4115."""
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        print(f"Processing page {page}/{LAST_PAGE}...")

        try:
            hashes = find_all_profiles(str(page))
        except Exception as e:
            print(f"  Error fetching hashes for page {page}: {e}")
            time.sleep(REQUEST_DELAY_SECONDS)
            continue

        if not hashes:
            print(f"  No profiles found on page {page}")
            time.sleep(REQUEST_DELAY_SECONDS)
            continue

        print(f"  Found {len(hashes)} profiles")

        for hash_value in hashes:
            profile = _safe_get_profile(hash_value)

            if profile is None:
                print(f"    Failed to fetch profile: {hash_value}")
                continue

            try:
                append_profile_to_csv(profile)
                print(f"    Saved: {profile.name}")
            except Exception as e:
                print(f"    Error saving profile {hash_value}: {e}")

            time.sleep(REQUEST_DELAY_SECONDS)

        time.sleep(REQUEST_DELAY_SECONDS)

    print("Harvest complete.")


if __name__ == "__main__":
    run_harvest()
