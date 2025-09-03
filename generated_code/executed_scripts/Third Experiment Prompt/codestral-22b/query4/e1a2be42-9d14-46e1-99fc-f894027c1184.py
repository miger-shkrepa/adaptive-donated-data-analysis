import os
import json
import csv

root_dir = "root_dir"
companies = set()

def extract_companies(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        for item in data.values():
                            if isinstance(item, list):
                                for sub_item in item:
                                    if 'string_map_data' in sub_item and 'Author' in sub_item['string_map_data']:
                                        companies.add(sub_item['string_map_data']['Author']['value'])
                except FileNotFoundError:
                    print(f"FileNotFoundError: The file {file} does not exist.")
                except json.JSONDecodeError:
                    print(f"JSONDecodeError: The file {file} is not a valid JSON file.")

extract_companies(os.path.join(root_dir, 'ads_information'))
extract_companies(os.path.join(root_dir, 'personal_information'))

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Company Name'])
    for company in companies:
        writer.writerow([company])