import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Initialize CSV writer
        csv_file = open('query_responses/results.csv', 'w', newline='')
        writer = csv.writer(csv_file)

        # Write CSV headers
        writer.writerow(["Changed", "New Value", "Change Date"])

        # Find personal information directory
        personal_info_dir = os.path.join(root_dir, "personal_information", "personal_information")
        if not os.path.exists(personal_info_dir):
            # If directory does not exist, return CSV with only headers
            csv_file.close()
            return

        # Find profile changes file
        profile_changes_file = os.path.join(personal_info_dir, "profile_changes.json")
        if not os.path.exists(profile_changes_file):
            # If file does not exist, return CSV with only headers
            csv_file.close()
            return

        # Read profile changes file
        with open(profile_changes_file, 'r') as f:
            profile_changes = json.load(f)

        # Extract changes
        changes = []
        for change in profile_changes["profile_profile_change"]:
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date = datetime.fromtimestamp(change["string_map_data"]["Change Date"]["timestamp"]).strftime("%Y-%m-%d")
            changes.append([changed, new_value, change_date])

        # Write changes to CSV
        writer.writerows(changes)

        csv_file.close()

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_account_changes(root_dir)