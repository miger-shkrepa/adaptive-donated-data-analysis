import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_directory):
    companies_with_access = set()

    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        for dirpath, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            if 'your_instagram_activity' in dirpath:
                                if 'comments' in dirpath or 'likes' in dirpath or 'avatars_store' in dirpath or 'events' in dirpath:
                                    for key, value in data.items():
                                        if isinstance(value, list):
                                            for item in value:
                                                if 'string_map_data' in item and 'Media Owner' in item['string_map_data']:
                                                    companies_with_access.add(item['string_map_data']['Media Owner']['value'])
                    except json.JSONDecodeError:
                        raise ValueError("Error: JSON file is not properly formatted.")
                    except FileNotFoundError:
                        raise FileNotFoundError("Error: JSON file not found.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    return companies_with_access

def write_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

try:
    companies_with_access = get_companies_with_access_to_instagram_activity(root_dir)
    write_to_csv(companies_with_access, 'query_responses/results.csv')
except Exception as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name'])