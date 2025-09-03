import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

try:
    with open(file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The required file does not exist.")
except json.JSONDecodeError:
    raise ValueError("ValueError: The file is not a valid JSON.")

results = []

for change in data.get("profile_profile_change", []):
    changed = change["string_map_data"].get("Changed", {}).get("value", "")
    new_value = change["string_map_data"].get("New Value", {}).get("value", "")
    change_date_timestamp = change["string_map_data"].get("Change Date", {}).get("timestamp", "")
    change_date = datetime.fromtimestamp(change_date_timestamp).strftime('%Y-%m-%d') if change_date_timestamp else ""

    results.append([changed, new_value, change_date])

output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(results)