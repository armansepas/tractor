import pandas as pd 

df = pd.read_excel("apps/wiki-tajrobeh/data/wiki-tajrobeh.xlsx")
print(f"Total rows in the dataset: {len(df)}")
print(df.head())
print(df.columns)

# Generate BI report with 3 sheets

# Sheet 1: Province - column A: province_name, column B: vendor_count
province_counts = df.groupby('province_name').size().reset_index(name='vendor_count').sort_values('vendor_count', ascending=False)

# Sheet 2: City - column A: city_name, column B: vendor_count
city_counts = df.groupby('city_name').size().reset_index(name='vendor_count').sort_values('vendor_count', ascending=False)

# Sheet 3: Category - column A: category_names, column B: vendor_count
category_counts = df.groupby('category_names').size().reset_index(name='vendor_count').sort_values('vendor_count', ascending=False)

# Write to Excel with 3 sheets
with pd.ExcelWriter('apps/wiki-tajrobeh/data/BI_report.xlsx') as writer:
    province_counts.to_excel(writer, sheet_name='Province', index=False)
    city_counts.to_excel(writer, sheet_name='City', index=False)
    category_counts.to_excel(writer, sheet_name='Category', index=False)

print("BI report generated: apps/wiki-tajrobeh/data/BI_report.xlsx")