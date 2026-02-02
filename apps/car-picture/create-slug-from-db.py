import pandas as pd
import re

def slugify(text):
    if not text:
        return ""
    # Convert to string and remove special characters
    text = str(text)
    # Remove special characters and keep only alphanumeric and spaces
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text.strip())
    # Remove multiple hyphens
    text = re.sub(r'-+', '-', text)
    # Make lowercase
    return text.lower()

# Read your CSV file
df = pd.read_csv('./apps/car-picture/data/all-db-cars.csv')

# Generate all slugs and add identifiers
results = []

for _, row in df.iterrows():
    # Get identifiers
    brand_id = int(row.get('CarBrandId', 0))
    model_id = int(row.get('CarModelId', 0))
    type_id = int(row.get('CarTypeId', 0))
    
    # Get text values
    brand_title = str(row.get('CarBrandTitleEn', '')).strip()
    model_title = str(row.get('CarModelTitleEn', '')).strip()
    year_persian = str(row.get('CarTypeYearPersian', '')).strip()
    year_georgian = str(row.get('CarTypeYearGeorgian', '')).strip()
    car_type = str(row.get('CarTypeTitle', '')).strip()
    
    # Create slugs
    slug1 = slugify(brand_title) + '-' + slugify(model_title)
    slug2 = slugify(brand_title) + '-' + slugify(model_title) + '-' + slugify(year_persian)
    slug3 = slugify(brand_title) + '-' + slugify(model_title) + '-' + slugify(year_georgian)
    slug4 = slugify(brand_title) + '-' + slugify(model_title) + '-' + (car_type).replace(' ', '-')
    
    # Create result object
    car_data = {
        "carBrandId": brand_id,
        "carModelId": model_id,
        "carTypeId": type_id,
        "brand": slugify(brand_title),
        "model": slugify(model_title),
        "year_persian": year_persian,
        "year_georgian": year_georgian,
        "car_type": car_type,
        "slug1": slug1,
        "slug2": slug2,
        "slug3": slug3,
        "slug4": slug4
    }
    
    results.append(car_data)

# Sort by brand, model, then type (alphabetically)
results.sort(key=lambda x: (x['brand'].lower(), x['model'].lower(), x['car_type']))

# Save to JSON file
import json
with open('./apps/car-picture/data/car_slugs_from_db.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Generated {len(results)} car records with slugs")
