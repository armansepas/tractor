import pandas as pd
import requests
import time
import os 

df = pd.read_json('data/image-links-with-slugs.json')
print("count: ", len(df))

failed_urls = []

for i, row in df.iterrows():
    url = row['imageHarvestUrl']
    name = row['fullSlug']
    print(i , ": " ,url)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            os.makedirs('data/bama-bg-pic', exist_ok=True)
            with open(f'data/bama-bg-pic/{name}.png', 'wb') as f:
                f.write(r.content)
            break  # Success, exit retry loop
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {name}: {e}. Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print(f"Error on {name} after {max_retries} attempts: {e}")
                failed_urls.append(url)
        
    time.sleep(2)

# Print failed URLs at the end
if failed_urls:
    print("\n\nFailed URLs:")
    for idx, url in enumerate(failed_urls, 1):
        print(f"{idx}. {url}")        