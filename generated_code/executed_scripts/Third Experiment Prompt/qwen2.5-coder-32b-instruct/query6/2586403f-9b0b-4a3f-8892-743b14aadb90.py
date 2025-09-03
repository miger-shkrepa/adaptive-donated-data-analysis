import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse timestamp
def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%MM-%d')
    except (ValueError, TypeError):
        return None

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Initialize a list to store the changes
changes = []

# Process signup_details.json
signup_details_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "signup_details.json")
if os.path.exists(signup_details_path):
    signup_details = read_json_file(signup_details_path)
    for entry in signup_details.get("account_history_registration_info", []):
        string_map_data = entry.get("string_map_data", {})
        for key, value in string_map_data.items():
            timestamp = value.get("timestamp")
            changes.append({
                "Changed": key,
                "New Value": value.get("value"),
                "Change Date": parse_timestamp(timestamp)
            })

# Process login_activity.json
login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
if os.path.exists(login_activity_path):
    login_activity = read_json_file(login_activity_path)
    for entry in login_activity.get("account_history_login_history", []):
        string_map_data = entry.get("string_map_data", {})
        for key, value in string_map_data.items():
            timestamp = value.get("timestamp")
            changes.append({
                "Changed": key,
                "New Value": value.get("value"),
                "Change Date": parse_timestamp(timestamp)
            })

# Ensure the output directory exists
output_dir = os.path.dirname("query_responses/results.csv")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write the changes to a CSV file
with open("query_responses/results.csv", 'w', newline='') as csvfile:
    fieldnames = ["Changed", "New Value", "Change Date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for change in changes:
        writer.writerow(change)