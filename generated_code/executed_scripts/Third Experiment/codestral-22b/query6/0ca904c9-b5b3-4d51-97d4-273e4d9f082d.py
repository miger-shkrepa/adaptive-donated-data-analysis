import os
import csv
from datetime import datetime

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

changes = []

# Assuming there is a JSON file containing account details
account_details_file = os.path.join(root_dir, "account_details.json")

if os.path.exists(account_details_file):
    with open(account_details_file, "r") as f:
        account_details = json.load(f)

    # Assuming the JSON file has a structure like this:
    # {"name": {"value": "old_name", "timestamp": "2022-01-01"}, ...}
    for key, details in account_details.items():
        if "old_value" in details:
            changes.append({
                "Changed": key,
                "New Value": details["value"],
                "Change Date": datetime.fromtimestamp(details["timestamp"]).strftime('%Y-%m-%d')
            })

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Changed', 'New Value', 'Change Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for change in changes:
        writer.writerow(change)