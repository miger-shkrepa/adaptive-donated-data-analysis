import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    changes = []

    # Check if the necessary files exist
    account_changes_file = os.path.join(root_dir, "account_changes.json")
    if not os.path.exists(account_changes_file):
        # If the file does not exist, create a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])
        print("CSV file created with only headers due to missing data.")
        exit()

    with open(account_changes_file, 'r') as file:
        data = json.load(file)

    # Assuming the structure of account_changes.json matches the provided structure
    for change_type, change_data in data.get("string_map_data", {}).items():
        for entry in change_data:
            timestamp = entry.get("timestamp")
            if timestamp is not None:
                change_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                new_value = entry.get("value")
                changes.append([change_type, new_value, change_date])

    # Write the changes to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
        writer.writerows(changes)

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding error - {e}")
except Exception as e:
    raise ValueError(f"Error: An unexpected error occurred - {e}")