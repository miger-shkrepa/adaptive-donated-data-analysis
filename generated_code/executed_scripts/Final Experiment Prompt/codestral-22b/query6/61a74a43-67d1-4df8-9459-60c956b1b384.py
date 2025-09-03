import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

def parse_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def get_profile_changes(file_path):
    changes = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        for change in data["profile_changes"]:
            for key, value in change["string_map_data"].items():
                changes.append({
                    "Changed": key,
                    "New Value": value["value"],
                    "Change Date": parse_date(value["timestamp"])
                })

    return changes

def save_to_csv(changes, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Changed", "New Value", "Change Date"])
        writer.writeheader()
        writer.writerows(changes)

try:
    changes = get_profile_changes(profile_changes_file)
    save_to_csv(changes, "query_responses/results.csv")
except Exception as e:
    print(f"Error: {e}")