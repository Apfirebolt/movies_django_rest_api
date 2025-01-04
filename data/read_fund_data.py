import json

# Path to the JSON file
file_path = 'data/funds.json'

# Read the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

    # Print the number of rows
print(f"Number of rows: {len(data)}")