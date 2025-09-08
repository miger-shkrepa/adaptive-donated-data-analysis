import os
import json
from datetime import datetime
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

if os.path.exists(profile_changes_file):
    with open(profile_changes_file, 'r') as f:
        data = json.load(f)
        for change in data["profile_profile_change"]:
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change.get("string_map_data", {}).get("New Value", {}).get("value", "")
            change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime('%Y-%m-%d')
            results.append([changed, new_value, change_date])

results.sort(key=lambda x: x[2])  # sort by change date

# write results to csv
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(results)