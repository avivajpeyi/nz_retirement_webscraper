import json

with open('../scraper/data.json', 'r') as file:
    data = json.load(file)

num_elements = len(data)
print("Number of pages in the JSON:", num_elements)