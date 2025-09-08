import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_directory):
    companies = set()
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for subdir, dirs, files in os.walk(root_directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            if "your_instagram_activity" in subdir:
                                for key, value in data.items():
                                    if isinstance(value, dict) and "string_map_data" in value:
                                        for sub_key, sub_value in value["string_map_data"].items():
                                            if "Company Name" in sub_key:
                                                companies.add(sub_value["value"])
                        except json.JSONDecodeError:
                            raise ValueError("Error: JSON decoding failed for file: " + file_path)
    except Exception as e:
        raise e

    return companies

def write_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

try:
    companies_with_access = get_companies_with_access(root_dir)
    write_to_csv(companies_with_access)
except Exception as e:
    print(e)