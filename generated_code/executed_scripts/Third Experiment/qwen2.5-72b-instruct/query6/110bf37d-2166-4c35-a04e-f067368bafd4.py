import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_account_changes():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        account_changes = []
        personal_info_path = os.path.join(root_dir, "personal_information", "account_based_in.json")

        if not os.path.exists(personal_info_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Changed', 'New Value', 'Change Date'])
            return

        with open(personal_info_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("inferred_data_primary_location", []):
                string_map_data = entry.get("string_map_data", {})
                for key, value in string_map_data.items():
                    if key == "Name der Stadt":
                        account_changes.append({
                            'Changed': 'Location',
                            'New Value': value.get("value"),
                            'Change Date': datetime.fromtimestamp(value.get("timestamp")).strftime('%Y-%m-%d')
                        })

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])
            for change in account_changes:
                writer.writerow([change['Changed'], change['New Value'], change['Change Date']])

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

get_account_changes()