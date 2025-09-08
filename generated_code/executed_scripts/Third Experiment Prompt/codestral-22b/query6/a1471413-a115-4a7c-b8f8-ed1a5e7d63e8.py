import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the changes
changes = []

# Define the path to the personal information file
personal_info_file = os.path.join(root_dir, "personal_information", "personal_information", "personal_information.json")

# Check if the personal information file exists
if os.path.exists(personal_info_file):
    # Load the personal information file
    with open(personal_info_file, "r") as f:
        data = json.load(f)

    # Extract the relevant information
    for item in data.get("profile_user", []):
        string_map_data = item.get("string_map_data", {})
        for key, value in string_map_data.items():
            if key in ["Name", "Phone Number", "Email"]:
                changes.append({
                    "Changed": key,
                    "New Value": value.get("value", ""),
                    "Change Date": datetime.fromtimestamp(value.get("timestamp", 0)).strftime("%Y-%m-%d")
                })

# Write the changes to a CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Changed", "New Value", "Change Date"])
    writer.writeheader()
    writer.writerows(changes)