import pandas as pd
import numpy as np
import requests
import os

images = {}
images["links"]=[]
images["slug"] =[]
images["title"] =[]

# Loop through each page of api 
for page in range(11):
    print("page Number:", page+1)
    res = requests.get(f"https://api2.zoomit.ir/catalog/api/products/search?pageNumber={page+1}&categorySlug=car").json()
    if not res["products"]["source"]:
        break
    length = len(res["products"]["source"])
    print("Number of items in this page:",length)
    for l in range(length):
        id = res["products"]["source"][l]["image"]["id"]
        image_url = f"https://api2.zoomit.ir/media/{id}"
        images["links"].append(image_url)
        images["slug"].append(res["products"]["source"][l]["slug"])
        images["title"].append(res["products"]["source"][l]["title"])
    print("all links in this page fetched")

print(f"all {page-1} links were successfully fetched!")

print("total link numbers:",len(images["links"]))
images_df = pd.DataFrame(images)
print("Links Dataframe:")
print(images_df)
images_df.to_csv("links.csv")
print("Links saved to links.csv file")
# print(images_df.iloc[0])
# print(images_df.iloc[0]["links"])

# Loop throug each page and get all car images, titles, and slugs from there
for i in range(len(images_df)):
    url = images_df.iloc[i]["links"]
    response = requests.get(url)
    if response.status_code == 200:
        folder_name = "downloaded_images"
        os.makedirs(folder_name, exist_ok=True)

        filename = images_df.iloc[i]["slug"].split("/")[-1].replace(",", "_")+ ".webp"
        full_path = os.path.join(folder_name, filename)  

        with open(full_path, "wb") as file:
            file.write(response.content)
        
        # print(f"فایل با موفقیت دانلود شد: {filename}")
    else:
        print(f"خطا در دانلود! کد وضعیت: {response.status_code}")

print(f"all {len(images_df)} were successfully downloaded!")