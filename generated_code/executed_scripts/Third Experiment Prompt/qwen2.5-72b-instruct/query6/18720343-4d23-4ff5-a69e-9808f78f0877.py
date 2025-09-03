import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_account_changes():
    changes = []

    try:
        personal_info_path = os.path.join(root_dir, "personal_information", "personal_information", "account_information.json")
        if os.path.exists(personal_info_path):
            account_info = load_json_file(personal_info_path)
            for entry in account_info["profile_account_insights"]:
                for key, value in entry["string_map_data"].items():
                    if "timestamp" in value:
                        timestamp = datetime.fromtimestamp(value["timestamp"] / 1000).strftime('%Y-%m-%d')
                        changes.append([key, value["value"], timestamp])
        else:
            print("Warning: account_information.json not found.")
    except Exception as e:
        print(f"Error processing account_information.json: {e}")

    return changes

def save_to_csv(changes):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Changed', 'New Value', 'Change Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        if changes:
            for change in changes:
                writer.writerow({'Changed': change[0], 'New Value': change[1], 'Change Date': change[2]})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        changes = get_account_changes()
        save_to_csv(changes)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()