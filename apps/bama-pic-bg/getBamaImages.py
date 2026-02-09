import pandas as pd
import requests
import time
import os 

df = pd.read_json('data/image-links-with-slugs.json')
print("count: ", len(df))

for i, row in df.iterrows():
    url = row['imageHarvestUrl']
    name = row['fullSlug']
    print(i , ": " ,url)
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        os.makedirs('data/bama-bg-pic', exist_ok=True)
        with open(f'data/bama-bg-pic/{name}.png', 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"Error on {name}: {e}")
        
    time.sleep(1)        