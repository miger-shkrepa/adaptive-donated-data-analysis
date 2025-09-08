import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Check if the necessary files exist
    account_changes_file = os.path.join(root_dir, "your_instagram_activity", "account_changes.json")
    if not os.path.exists(account_changes_file):
        # If the file does not exist, create a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print("CSV file created with only headers as the required file does not exist.")
    else:
        # If the file exists, process it
        with open(account_changes_file, 'r') as file:
            data = json.load(file)

        # Prepare the data for the CSV
        changes = []
        for change in data.get('account_changes', []):
            for key, value in change.get('string_list_data', {}).items():
                changes.append({
                    'Changed': key,
                    'New Value': value.get('value', ''),
                    'Change Date': datetime.fromtimestamp(value.get('timestamp', 0)).strftime('%Y-%m-%d')
                })

        # Write the data to the CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)

        print("CSV file created with the account changes data.")
except FileNotFoundError as e:
    print(e)
except Exception as e:
    raise ValueError(f"Error: {str(e)}")