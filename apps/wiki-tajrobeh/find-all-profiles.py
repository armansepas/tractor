import requests as req

def find_all_profiles(page : str) -> list[str]:
    base_url = f'https://tajrobe.wiki/api/client/category/228/profiles?sort=desc&page={page}'
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WikiTajrobeHarvester/1.0)",
        "Accept": "application/json",
    }
    response = req.get(base_url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    profiles = data.get("data", [])
    if len(profiles) == 0:
        return []
    else:
        return [profile.get("hash") for profile in profiles]
    

data = find_all_profiles("1")
print(data)