import os
import json
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

companies = set()

# Function to extract company names from a JSON file
def extract_companies(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if "structure" in data:
                structure = data["structure"]
                if isinstance(structure, list):
                    for item in structure:
                        if "string_map_data" in item and "Author" in item["string_map_data"]:
                            companies.add(item["string_map_data"]["Author"]["value"])
                elif isinstance(structure, dict):
                    for key, value in structure.items():
                        if isinstance(value, list):
                            for item in value:
                                if "string_map_data" in item and "Author" in item["string_map_data"]:
                                    companies.add(item["string_map_data"]["Author"]["value"])
    except Exception as e:
        raise type(e)(f"Error: {str(e)}")

# Walk through the directory
for foldername, subfolders, filenames in os.walk(root_dir):
    if "ads_information" in foldername or "preferences" in foldername:
        for filename in filenames:
            if filename.endswith('.json'):
                extract_companies(os.path.join(foldername, filename))

# Write the results to a CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])