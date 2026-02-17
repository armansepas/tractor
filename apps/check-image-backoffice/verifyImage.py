import pandas as pd 
import requests as req


df = pd.read_excel('apps/check-image-backoffice/data/Arma.xlsx')

df["isOk"] = ""

print(df.head())

base_url = "https://minioapi.yadak.com/public-dev/"

for i in range(len(df)):
    imageUrl = df.loc[i, "AttachmentUrl"]
    print(imageUrl)
    response = req.get(base_url + imageUrl)
    if response.status_code == 200:
        df.loc[i, "isOk"] = "True"
    else:
        df.loc[i, "isOk"] = "False"

print(df.head())

df.to_excel('apps/check-image-backoffice/data/Arma_result.xlsx', index=False)