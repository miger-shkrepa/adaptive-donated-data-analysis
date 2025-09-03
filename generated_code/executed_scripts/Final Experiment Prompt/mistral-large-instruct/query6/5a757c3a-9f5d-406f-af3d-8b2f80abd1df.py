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

# Function to convert timestamp to 'YYYY-MM-DD' format
def convert_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return "Invalid Date"

# Initialize the CSV writer with the required headers
csv_headers = ["Changed", "New Value", "Change Date"]
csv_data = [csv_headers]

try:
    # Check if the profile changes file exists
    if not os.path.exists(profile_changes_path):
        raise FileNotFoundError("FileNotFoundError: The profile changes file does not exist.")

    # Read the profile changes JSON file
    with open(profile_changes_path, 'r') as file:
        profile_changes = json.load(file)

    # Extract the required data from the JSON
    for change in profile_changes.get("profile_profile_change", []):
        string_map_data = change.get("string_map_data", {})
        changed = string_map_data.get("Changed", {}).get("value", "")
        new_value = string_map_data.get("New Value", {}).get("value", "")
        change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", "")

        # Convert the timestamp to 'YYYY-MM-DD' format
        change_date = convert_timestamp(change_date_timestamp)

        # Append the extracted data to the CSV data
        csv_data.append([changed, new_value, change_date])

except FileNotFoundError as fnf_error:
    print(fnf_error)
except json.JSONDecodeError:
    raise ValueError("Error: The profile changes file is not a valid JSON.")
except Exception as e:
    raise ValueError(f"Error: {str(e)}")

# Write the CSV data to the output file
try:
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
except Exception as e:
    raise ValueError(f"Error: Unable to write to the output CSV file. {str(e)}")