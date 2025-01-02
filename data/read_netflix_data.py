import pandas as pd

# Read the CSV file
file_path = 'data/netflix_titles.csv'
data = pd.read_csv(file_path)

# Print the number of rows
print(f"Number of rows: {len(data)}")

# Print all column names
print("Column names:", data.columns.tolist())

# Print the first 5 rows
# print(data.head())

# print the data type of release_year and check how many null values are there
# print(data['release_year'].dtype)
# print(data['release_year'].isnull().sum())

# print the data type of date_added and check how many null values are there
print(data['date_added'].dtype)
print(data['date_added'].isnull().sum())

# print date_added and release_year, rating, duration for first 100 rows
# print(data[['date_added', 'release_year', 'rating', 'duration']].head(100))

# print type, title, director, cast and country for first 100 rows
# print(data[['type', 'title', 'director', 'cast', 'country']].head(100))