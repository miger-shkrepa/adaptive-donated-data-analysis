import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def convert_timestamp_to_date(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (TypeError, OSError):
        raise ValueError("Error: Invalid timestamp value.")

def process_profile_changes(data):
    changes = []
    for entry in data.get("profile_profile_change", []):
        string_map_data = entry.get("string_map_data", {})
        changed = string_map_data.get("Changed", {}).get("value", "")
        new_value = string_map_data.get("New Value", {}).get("value", "")
        change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)
        change_date = convert_timestamp_to_date(change_date_timestamp) if change_date_timestamp else ""
        changes.append([changed, new_value, change_date])
    return changes

def write_to_csv(changes, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
        writer.writerows(changes)

def main():
    try:
        file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        if not os.path.exists(file_path):
            write_to_csv([], 'query_responses/results.csv')
            return

        data = load_json_data(file_path)
        changes = process_profile_changes(data)
        write_to_csv(changes, 'query_responses/results.csv')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()