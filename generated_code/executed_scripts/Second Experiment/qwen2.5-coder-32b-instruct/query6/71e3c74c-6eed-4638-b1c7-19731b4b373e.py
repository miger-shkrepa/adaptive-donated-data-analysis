import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_file_path(directory, file_name):
    return os.path.join(directory, file_name)

def read_json_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        import json
        return json.load(file)

def extract_changes(data):
    changes = []
    for entry in data.get('profile_account_insights', []):
        string_map_data = entry.get('string_map_data', {})
        for key, value in string_map_data.items():
            timestamp = value.get('timestamp')
            if timestamp:
                change_date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                changes.append({'Changed': key, 'New Value': value.get('value'), 'Change Date': change_date})
    return changes

def main():
    try:
        instagram_profile_path = get_file_path(root_dir, 'personal_information/instagram_profile_information.json')
        instagram_data = read_json_file(instagram_profile_path)
        changes = extract_changes(instagram_data)
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while processing the data: {str(e)}")

if __name__ == "__main__":
    main()