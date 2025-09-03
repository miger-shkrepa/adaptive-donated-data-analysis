import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the input JSON file
input_file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Define the path to the output CSV file
output_file_path = "query_responses/results.csv"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Function to convert timestamp to 'YYYY-MM-DD' format
def convert_timestamp(timestamp):
    try:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return "Invalid Date"

# Initialize the CSV writer
with open(output_file_path, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Changed", "New Value", "Change Date"])

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        raise FileNotFoundError("FileNotFoundError: The input file does not exist.")

    # Read the JSON file
    try:
        with open(input_file_path, 'r') as jsonfile:
            data = json.load(jsonfile)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The input file is not a valid JSON.")

    # Extract the required data
    try:
        profile_changes = data.get("profile_profile_change", [])
        for change in profile_changes:
            string_map_data = change.get("string_map_data", {})
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", "")
            change_date = convert_timestamp(change_date_timestamp)

            csv_writer.writerow([changed, new_value, change_date])
    except (KeyError, TypeError) as e:
        raise ValueError(f"ValueError: Error processing the JSON data - {str(e)}")

print(f"Results have been written to {output_file_path}")