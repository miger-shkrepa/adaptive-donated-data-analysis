import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Define the path to the account_changes.json file
    account_changes_path = os.path.join(root_dir, "account_changes.json")

    # Check if the account_changes.json file exists
    if not os.path.exists(account_changes_path):
        # If the file does not exist, create a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Changed', 'New Value', 'Change Date'])
    else:
        # If the file exists, read the JSON data
        with open(account_changes_path, 'r') as jsonfile:
            data = json.load(jsonfile)

        # Prepare the data for the CSV file
        changes = []
        for change in data.get('account_changes', []):
            for key, value in change.get('string_map_data', {}).items():
                changes.append([key, value.get('value'), datetime.fromtimestamp(value.get('timestamp')).strftime('%Y-%m-%d')])

        # Write the data to the CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Changed', 'New Value', 'Change Date'])
            csvwriter.writerows(changes)

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding error - {e}")
except Exception as e:
    raise ValueError(f"Error: An unexpected error occurred - {e}")