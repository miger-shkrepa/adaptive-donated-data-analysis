import os
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def convert_timestamp_to_date(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (OSError, OverflowError, ValueError):
        raise ValueError(f"ValueError: The timestamp {timestamp} is invalid.")

def extract_profile_changes(data):
    changes = []
    for entry in data.get("profile_profile_change", []):
        string_map_data = entry.get("string_map_data", {})
        changed = string_map_data.get("Changed", {}).get("value", "")
        new_value = string_map_data.get("New Value", {}).get("value", "")
        change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)
        change_date = convert_timestamp_to_date(change_date_timestamp) if change_date_timestamp else ""
        changes.append((changed, new_value, change_date))
    return changes

def write_csv_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("Changed,New Value,Change Date\n")
            for changed, new_value, change_date in data:
                file.write(f"{changed},{new_value},{change_date}\n")
    except IOError:
        raise IOError(f"IOError: Failed to write to the file {file_path}.")

def main():
    json_file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
    csv_file_path = "query_responses/results.csv"
    
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Read the JSON file
        data = read_json_file(json_file_path)
        
        # Extract profile changes
        changes = extract_profile_changes(data)
        
        # Write the CSV file
        write_csv_file(csv_file_path, changes)
        
    except (FileNotFoundError, ValueError, IOError) as e:
        # If any error occurs, write only the column headers to the CSV file
        write_csv_file(csv_file_path, [])

if __name__ == "__main__":
    main()