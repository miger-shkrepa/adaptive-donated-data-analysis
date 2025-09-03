import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the profile changes JSON file
profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Function to convert timestamp to 'YYYY-MM-DD' format
def convert_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (ValueError, OSError) as e:
        raise ValueError(f"Error: Invalid timestamp value - {e}")

# Initialize the CSV writer
with open(output_csv_path, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Changed", "New Value", "Change Date"])

    # Check if the profile changes file exists
    if not os.path.exists(profile_changes_path):
        raise FileNotFoundError("FileNotFoundError: The profile changes file does not exist.")

    # Read the profile changes JSON file
    try:
        with open(profile_changes_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise FileNotFoundError(f"Error: Unable to read or parse the profile changes file - {e}")

    # Extract the required data and write to CSV
    try:
        profile_changes = data.get("profile_profile_change", [])
        for change in profile_changes:
            string_map_data = change.get("string_map_data", {})
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)
            change_date = convert_timestamp(change_date_timestamp)

            csv_writer.writerow([changed, new_value, change_date])
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error: Missing or invalid data in the profile changes file - {e}")