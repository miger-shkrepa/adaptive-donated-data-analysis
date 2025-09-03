import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_profile_changes(data):
    changes = []
    for entry in data.get("profile_profile_change", []):
        change_date = entry["string_map_data"].get("Change Date", {}).get("value")
        if change_date:
            change_date = datetime.fromtimestamp(int(change_date)).strftime('%Y-%m-%d')
        else:
            change_date = None
        new_value = entry["string_map_data"].get("New Value", {}).get("value")
        changed = entry["string_map_data"].get("Changed", {}).get("value")
        if change_date and new_value and changed:
            changes.append({"Changed": changed, "New Value": new_value, "Change Date": change_date})
    return changes

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        profile_changes_path = os.path.join(root_dir, "personal_information", "profile_changes.json")
        if not os.path.exists(profile_changes_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["Changed", "New Value", "Change Date"])
                writer.writeheader()
            return

        with open(profile_changes_path, 'r') as file:
            data = json.load(file)
        
        changes = process_profile_changes(data)
        
        if not changes:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["Changed", "New Value", "Change Date"])
                writer.writeheader()
            return

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Changed", "New Value", "Change Date"])
            writer.writeheader()
            for change in changes:
                writer.writerow(change)

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    main()