import pandas as pd

# Read the CSV file
file_path = 'data/anime-data.csv'
df = pd.read_csv(file_path)

print(df.head())

# for index, row in df.iterrows():
#     if index >= 5:
#         break
#     print(f"Name: {row['name']}, Diet: {row['diet']}, Period: {row['period']}, Length: {row['length']}, Taxonomy: {row['taxonomy']}, Named By: {row['named_by']}, Species: {row['species']}")

# # Column Names: ['name', 'diet', 'period', 'lived_in', 'type', 'length', 'taxonomy', 'named_by', 'species', 'link']