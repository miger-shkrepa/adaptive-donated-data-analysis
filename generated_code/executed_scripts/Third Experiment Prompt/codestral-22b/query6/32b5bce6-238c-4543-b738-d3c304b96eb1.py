import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

account_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

if os.path.exists(account_changes_file):
    with open(account_changes_file, 'r') as f:
        data = json.load(f)
        for change in data["profile_profile_change"]:
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
            results.append([changed, new_value, change_date])

output_file = "query_responses/results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(results)