import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

changes = []

# Define the paths to the relevant JSON files
personal_info_path = os.path.join(root_dir, "personal_information", "personal_information", "personal_information.json")

# Check if the personal information file exists
if os.path.exists(personal_info_path):
    with open(personal_info_path, "r") as f:
        data = json.load(f)

    # Extract the relevant information
    for item in data["profile_user"]:
        name = item["string_map_data"].get("Name", {}).get("value", "")
        phone = item["string_map_data"].get("Telefonnummer", {}).get("value", "")
        email = item["string_map_data"].get("E-Mail-Adresse", {}).get("value", "")
        timestamp = item["string_map_data"].get("Name", {}).get("timestamp", "")

        # Convert the timestamp to a date
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d') if timestamp else ""

        # Add the information to the changes list
        changes.append(["Name", name, date])
        changes.append(["Phone", phone, date])
        changes.append(["Email", email, date])

# Write the changes to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)