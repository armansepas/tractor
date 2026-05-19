import pandas as pd 

df = pd.read_csv("apps/behtarino/data/behtarino_business_data.csv")

df.to_excel("apps/behtarino/data/behtarino_automotives_whole_country.xlsx" , index=False)

