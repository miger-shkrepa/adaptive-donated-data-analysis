import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    output_data = [["Changed", "New Value", "Change Date"]]

    # Check if the necessary files exist
    account_changes_file = os.path.join(root_dir, "account_changes.json")
    if not os.path.exists(account_changes_file):
        # If the file does not exist, return a CSV with only headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(output_data)
        print("CSV file created with headers only.")
        exit()

    with open(account_changes_file, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Error: JSON data is not properly formatted.")

    # Assuming the structure of account_changes.json is similar to other JSON files provided
    if "account_changes" in data:
        for change in data["account_changes"]:
            if "changed_field" in change and "new_value" in change and "change_timestamp" in change:
                changed_field = change["changed_field"]
                new_value = change["new_value"]
                change_date = datetime.fromtimestamp(change["change_timestamp"]).strftime('%Y-%m-%d')
                output_data.append([changed_field, new_value, change_date])

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_data)

    print("CSV file created successfully.")

except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error: An unexpected error occurred: {e}")