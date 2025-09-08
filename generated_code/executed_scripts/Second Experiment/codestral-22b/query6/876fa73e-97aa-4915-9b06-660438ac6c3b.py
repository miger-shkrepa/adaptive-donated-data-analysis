import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the changes
changes = []

# Define the path to the personal_information.json file
personal_info_path = os.path.join(root_dir, "personal_information", "personal_information.json")

# Check if the personal_information.json file exists
if os.path.exists(personal_info_path):
    # Load the JSON data from the file
    with open(personal_info_path, 'r') as f:
        data = json.load(f)

    # Extract the relevant information
    for item in data.get("structure", {}).get("profile_user", []):
        string_map_data = item.get("string_map_data", {})
        for key, value in string_map_data.items():
            if key in ["Bio", "Date of birth"]:
                changes.append({
                    "Changed": key,
                    "New Value": value.get("value", ""),
                    "Change Date": datetime.fromtimestamp(value.get("timestamp", 0)).strftime('%Y-%m-%d')
                })

# Define the path to the instagram_profile_information.json file
instagram_info_path = os.path.join(root_dir, "personal_information", "instagram_profile_information.json")

# Check if the instagram_profile_information.json file exists
if os.path.exists(instagram_info_path):
    # Load the JSON data from the file
    with open(instagram_info_path, 'r') as f:
        data = json.load(f)

    # Extract the relevant information
    for item in data.get("structure", {}).get("profile_account_insights", []):
        string_map_data = item.get("string_map_data", {})
        for key, value in string_map_data.items():
            if key in ["Contact Syncing", "First Country Code"]:
                changes.append({
                    "Changed": key,
                    "New Value": value.get("value", ""),
                    "Change Date": datetime.fromtimestamp(value.get("timestamp", 0)).strftime('%Y-%m-%d')
                })

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Changed", "New Value", "Change Date"])
    writer.writeheader()
    writer.writerows(changes)