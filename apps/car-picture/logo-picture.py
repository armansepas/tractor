import pandas as pd 
import requests as req
import os 
from PIL import Image
import io

# Fetch the brands list
brandsResponse = req.get('https://khodro45.com/api/v1/brands/used-cars/?limit=250')
brands = brandsResponse.json()['results']

# Define folders for saving images and SVGs
image_folder = 'apps/car-picture/data/logo-image/images'
svg_folder = 'apps/car-picture/data/logo-image/svgs'

os.makedirs(image_folder, exist_ok=True)
os.makedirs(svg_folder, exist_ok=True)

# Download logos
for brand in brands:
    title_en = brand.get('title_en', 'unknown').lower().replace(' ', '_')
    
    # Download PNG logo
    image_url = brand.get('logo', {}).get('url')
    if image_url:
        try:
            response = req.get(image_url)
            if response.status_code == 200:
                # Convert PNG to WebP and save
                webp_path = os.path.join(image_folder, f"{title_en}.webp")
                image = Image.open(io.BytesIO(response.content))
                image.save(webp_path, 'WEBP')
                print(f"Converted and saved WebP: {webp_path}")
        except Exception as e:
            print(f"Failed to download/convert {title_en}: {e}")

    # Download SVG logo
    svg_url = brand.get('svg_logo', {}).get('url')
    if svg_url:
        try:
            response = req.get(svg_url)
            if response.status_code == 200:
                file_path = os.path.join(svg_folder, f"{title_en}.svg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded SVG: {file_path}")
        except Exception as e:
            print(f"Failed to download SVG for {title_en}: {e}")


# ===== PURE PNG 


# import pandas as pd 
# import requests as req
# import os 
# import json

# # Fetch the brands list
# brandsResponse = req.get('https://khodro45.com/api/v1/brands/used-cars/?limit=250')
# brands = brandsResponse.json()['results']

# # Define folders for saving images and SVGs
# image_folder = 'apps/car-picture/data/logo-image/images'
# svg_folder = 'apps/car-picture/data/logo-image/svgs'

# os.makedirs(image_folder, exist_ok=True)
# os.makedirs(svg_folder, exist_ok=True)

# # Download logos
# for brand in brands:
#     title_en = brand.get('title_en', 'unknown').lower().replace(' ', '_')
    
#     # Download PNG logo
#     image_url = brand.get('logo', {}).get('url')
#     if image_url:
#         try:
#             response = req.get(image_url)
#             if response.status_code == 200:
#                 file_path = os.path.join(image_folder, f"{title_en}.png")
#                 with open(file_path, 'wb') as f:
#                     f.write(response.content)
#                 print(f"Downloaded PNG: {file_path}")
#         except Exception as e:
#             print(f"Failed to download PNG for {title_en}: {e}")

#     # Download SVG logo
#     svg_url = brand.get('svg_logo', {}).get('url')
#     if svg_url:
#         try:
#             response = req.get(svg_url)
#             if response.status_code == 200:
#                 file_path = os.path.join(svg_folder, f"{title_en}.svg")
#                 with open(file_path, 'wb') as f:
#                     f.write(response.content)
#                 print(f"Downloaded SVG: {file_path}")
#         except Exception as e:
#             print(f"Failed to download SVG for {title_en}: {e}")


