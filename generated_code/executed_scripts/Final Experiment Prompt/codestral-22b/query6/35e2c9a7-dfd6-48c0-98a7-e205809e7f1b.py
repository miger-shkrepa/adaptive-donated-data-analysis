import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

if not os.path.exists(file_path):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Changed", "New Value", "Change Date"])
    print("The file does not exist, but the CSV file with headers has been created.")
else:
    with open(file_path, 'r') as file:
        data = json.load(file)

    changes = []
    for change in data["profile_profile_change"]:
        changed = change["string_map_data"]["Changed"]["value"]
        new_value = change["string_map_data"]["New Value"]["value"]
        timestamp = change["string_map_data"]["Change Date"]["timestamp"]
        change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        changes.append([changed, new_value, change_date])

    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Changed", "New Value", "Change Date"])
        writer.writerows(changes)

    print("The CSV file has been created successfully.")