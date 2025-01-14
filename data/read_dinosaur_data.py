import pandas as pd

# Read the CSV file
file_path = 'data/dinosaur.csv'
df = pd.read_csv(file_path)

# Print all column names
print("Column Names:", df.columns.tolist())

# Print the first 10 rows
print("First 10 Rows:")

for index, row in df.iterrows():
    if index >= 5:
        break
    print(f"Name: {row['name']}, Diet: {row['diet']}, Period: {row['period']}, Length: {row['length']}, Taxonomy: {row['taxonomy']}, Named By: {row['named_by']}, Species: {row['species']}")

# Column Names: ['name', 'diet', 'period', 'lived_in', 'type', 'length', 'taxonomy', 'named_by', 'species', 'link']