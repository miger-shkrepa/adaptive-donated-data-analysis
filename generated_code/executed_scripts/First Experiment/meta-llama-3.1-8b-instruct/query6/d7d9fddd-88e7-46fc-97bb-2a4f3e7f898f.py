import csv
import os
import json
from datetime import datetime

def get_instagram_changes(root_dir):
    instagram_changes = []
    for filename in os.listdir(root_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(root_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'instagram_profile_information.json' in filename:
                        for profile in data['profile_account_insights']:
                            for key, value in profile['string_map_data'].items():
                                if key in ['Contact Syncing', 'First Close Friends Story Time', 'First Country Code', 'First Story Time', 'Has Shared Live Video', 'Last Login', 'Last Logout', 'Last Story Time']:
                                    instagram_changes.append({
                                        'Changed': key,
                                        'New Value': value['value'],
                                        'Change Date': datetime.fromtimestamp(value['timestamp']).strftime('%Y-%m-%d')
                                    })
            except json.JSONDecodeError as e:
                raise ValueError("Error: Invalid JSON in file " + file_path)
            except FileNotFoundError as e:
                raise FileNotFoundError("FileNotFoundError: The file " + file_path + " does not exist.")
    return instagram_changes

def main():
    root_dir = "root_dir"
    try:
        instagram_changes = get_instagram_changes(root_dir)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Changed', 'New Value', 'Change Date'])
            writer.writeheader()
            writer.writerows(instagram_changes)
    except FileNotFoundError as e:
        raise e
    except ValueError as e:
        raise e

if __name__ == "__main__":
    main()