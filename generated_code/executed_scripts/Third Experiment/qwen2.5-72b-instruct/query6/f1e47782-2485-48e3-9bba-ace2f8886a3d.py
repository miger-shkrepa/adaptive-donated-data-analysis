import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_profile_changes(data):
    changes = []
    try:
        profile_changes = data["personal_information"]["profile_changes.json"]["structure"]["profile_profile_change"]
        for change in profile_changes:
            string_data = change["string_map_data"]
            change_date = datetime.fromtimestamp(string_data["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
            changes.append({
                "Changed": string_data["Changed"]["value"],
                "New Value": string_data["New Value"]["value"],
                "Change Date": change_date
            })
    except KeyError:
        pass  # If the key is not found, simply continue without adding any changes.
    return changes

def write_to_csv(changes):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        profile_changes_path = os.path.join(root_dir, "personal_information", "profile_changes.json")
        if not os.path.exists(profile_changes_path):
            write_to_csv([])  # Write CSV with headers only if the file is missing.
            return

        data = load_json_file(profile_changes_path)
        changes = get_profile_changes(data)
        write_to_csv(changes)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()