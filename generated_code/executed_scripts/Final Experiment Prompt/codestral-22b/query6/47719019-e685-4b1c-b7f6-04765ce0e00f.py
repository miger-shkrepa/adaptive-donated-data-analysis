import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
file_path = os.path.join(root_dir, "personal_information", "personal_information", "personal_information.json")

if not os.path.exists(file_path):
    data = []
    print("Error: The personal_information.json file does not exist.")
else:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []
        print("Error: The personal_information.json file is not a valid JSON file.")

changes = []
if 'profile_user' in data:
    for change in data['profile_user']:
        for field, details in change['string_map_data'].items():
            changes.append({
                'Changed': field,
                'New Value': details['value'],
                'Change Date': datetime.fromtimestamp(details['timestamp']).strftime('%Y-%m-%d')
            })

output_file = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Changed', 'New Value', 'Change Date'])
    writer.writeheader()
    writer.writerows(changes)