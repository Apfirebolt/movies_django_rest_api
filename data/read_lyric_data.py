import pandas as pd
import json

# Read the CSV file
file_path = 'data/lyrics.csv'
data = pd.read_csv(file_path)

# Print first row as json
print(data.iloc[0].to_json())

# Print all the columns of the data
print(data.columns)

# Print the shape of the data
print(data.shape)

# Print null values in the data for each column
print(data.isnull().sum())

# Print the number of rows where Year is -1
print(data[data['Year'] == -1].shape[0])

# Print the number of rows where Year after 2000
print(data[data['Year'] > 2000].shape[0])