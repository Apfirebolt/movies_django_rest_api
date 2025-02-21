import pandas as pd
import json

# Read the CSV file
file_path = 'data/planets.csv'
data = pd.read_csv(file_path)

# Print the first 5 rows and all columns
print(data.head())

# Print the shape of the data
print(data.shape)

# Print the columns of the data
print(data.columns)

# Print the first row in form of a dictionary
print(data.iloc[0].to_dict())