import pandas as pd

# Read the CSV file
file_path = 'data/movies.csv'
data = pd.read_csv(file_path)

# Print the first 10 rows
print(data.head(10))

# Print all the columns of the data
print(data.shape)