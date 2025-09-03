import os
import csv
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    personal_info_dir = os.path.join(root_dir, "personal_information")
    if not os.path.exists(personal_info_dir):
        raise FileNotFoundError("FileNotFoundError: The personal information directory does not exist.")

    profile_changes_file = os.path.join(personal_info_dir, "profile_changes.json")
    if not os.path.exists(profile_changes_file):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print("The necessary file does not exist in the structure. Returning a CSV file with only the column headers.")
    else:
        with open(profile_changes_file, 'r') as file:
            import json
            data = json.load(file)

        changes = []
        for change in data['profile_profile_change']:
            changed = change['string_map_data']['Changed']
            new_value = change['string_map_data']['New Value']
            change_date_timestamp = change['string_map_data']['Change Date']['timestamp']
            change_date = datetime.fromtimestamp(change_date_timestamp).strftime('%Y-%m-%d')
            changes.append({
                'Changed': changed,
                'New Value': new_value,
                'Change Date': change_date
            })

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)

except FileNotFoundError as e:
    raise FileNotFoundError(f"Error: {e}")
except json.JSONDecodeError as e:
    raise ValueError(f"Error: {e}")
except KeyError as e:
    raise ValueError(f"Error: {e}")
except Exception as e:
    raise Exception(f"Error: {e}")