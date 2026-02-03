import pandas as pd



df = pd.read_csv("apps/wiki-tajrobeh/data/profiles.csv")

# print(df.count())
print("harvested_from_url" , df["harvested_from_url"].nunique())
print("phone_numbers:", df["phone_numbers"].nunique())
print("lat" , df["lat"].nunique())
df = df.drop_duplicates(subset=["harvested_from_url"], keep="first").reset_index(drop=True)
# print(df.count())
df = (df.sort_values(["province_name","city_name"]).reset_index(drop=True))


df.to_excel("apps/wiki-tajrobeh/data/wiki-tajrobeh.xlsx", index=False)

# print(df.head())