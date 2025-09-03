import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

changes = []

signup_details_path = os.path.join(root_dir, "signup_details.json")
if os.path.exists(signup_details_path):
    with open(signup_details_path, 'r') as f:
        data = json.load(f)
        for change in data["account_history_registration_info"]:
            for key, value in change["string_map_data"].items():
                changes.append({
                    "Changed": key,
                    "New Value": value["value"],
                    "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime('%Y-%m-%d')
                })

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Changed", "New Value", "Change Date"])
    writer.writeheader()
    writer.writerows(changes)