import pandas as pd 
import requests as req
import os 
import json



brandsResponse = req.get('https://khodro45.com/api/v1/brands/used-cars/?limit=250')

brands = brandsResponse.json()['results']

# print(brands)

image_folder = 'app/car-pictures/logo-image/images'
svg_folder = 'app/car-pictures/logo-image/svgs'

os.makedirs(image_folder, exist_ok=True)
os.makedirs(svg_folder, exist_ok=True)



# # get brand logos 1- image jpeg 2- svg | different looking images 
# for b in brands : 
#     image = b['logo']['url']
#     svg = b['svg_logo']['url']

#     response = req.get(image)
#     os.




allBrands = []

for b in brands :
    allBrands.append({
        'id' : b['id'],
        'title_en' : b['title_en']
    })


# print(allBrands)

allModels = []

for a in allBrands:
    response = req.get(f"https://khodro45.com/api/v1/models/used-cars/?brand_id={a['id']}").json()
    for i in response:
        allModels.append({
            'model_id': i['id'],
            'brand_id': i['brand_id'],
        })


allYears = []

for m in allModels:
    response = req.get(f"https://khodro45.com/api/v1/years/used-cars/?model_id={m['model_id']}").json()
    for i in response:
        allYears.append({
            'model_id': m['model_id'],
            'year_id' : i['id']
        })
        print({
            'model_id': m['model_id'],
            'year_id' : i['id']
        })

allSeoSlug = [] 

for y in allYears :
    response = req.get(f"https://khodro45.com/api/v1/trims/used-cars/?model_id={y['model_id']}&year_id={y['year_id']}").json()
    for index, i in enumerate(response): 
        allSeoSlug.append({
            'model_id': y['model_id'],
            'year_id' : y['year_id'],
            'seo_slug' : i['seo_slug']
        })
        print({
            'model_id': y['model_id'],
            'year_id' : y['year_id'],
            'seo_slug' : i['seo_slug']
        })

my_data = {}

for index, i in enumerate(allSeoSlug): 
        my_data[index]={
            'model_id': i['model_id'],
            'year_id' : i['year_id'],
            'seo_slug' : i['seo_slug']
        }

# print(allYears)

# with open('data.json')
# allSeoSlug.``


with open("data.json", "w", encoding="utf-8") as file:
    json.dump(my_data, file, indent=4, ensure_ascii=False)