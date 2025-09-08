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

try:
    for change in data["profile_profile_change"]:
        changed = change["string_map_data"]["Changed"]["value"]
        new_value = change["string_map_data"]["New Value"]["value"]
        change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
        results.append([changed, new_value, change_date])
except KeyError:
    raise ValueError("ValueError: The JSON structure is not as expected.")

output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(results)