import pandas as pd

# Read the CSV file
file_path = 'data/books.csv'
data = pd.read_csv(file_path)

# Print the number of rows
print(f"Number of rows: {len(data)}")

# Print all column names
print("Column names:", data.columns.tolist())

# print null values in each column
print(data.isnull().sum())

# print price, publish date and publish year columns of first 5 rows
print(data[['Price Starting With ($)', 'Publish Date (Month)', 'Publish Date (Year)']].head())