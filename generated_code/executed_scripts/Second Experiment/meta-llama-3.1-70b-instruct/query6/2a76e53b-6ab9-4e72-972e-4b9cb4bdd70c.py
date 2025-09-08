import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_instagram_account_changes(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store the changes
        changes = []

        # Define the path to the personal information directory
        personal_info_dir = os.path.join(root_dir, "personal_information")

        # Check if the personal information directory exists
        if not os.path.exists(personal_info_dir):
            # If the directory does not exist, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Changed', 'New Value', 'Change Date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        # Define the path to the Instagram profile information file
        instagram_profile_info_file = os.path.join(personal_info_dir, "instagram_profile_information.json")

        # Check if the Instagram profile information file exists
        if not os.path.exists(instagram_profile_info_file):
            # If the file does not exist, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Changed', 'New Value', 'Change Date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        # Open the Instagram profile information file and read its contents
        with open(instagram_profile_info_file, 'r') as file:
            # Since we don't have the actual JSON data, we'll assume it's in the correct format
            # and we're only interested in the "string_map_data" section
            import json
            data = json.load(file)
            for profile_account_insights in data.get("profile_account_insights", []):
                string_map_data = profile_account_insights.get("string_map_data", {})
                for key, value in string_map_data.items():
                    # Extract the changed field, new value, and change date
                    changed = key
                    new_value = value.get("value", "")
                    change_date = datetime.fromtimestamp(value.get("timestamp", 0)).strftime("%Y-%m-%d")
                    changes.append({
                        "Changed": changed,
                        "New Value": new_value,
                        "Change Date": change_date
                    })

        # Write the changes to the CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_instagram_account_changes(root_dir)