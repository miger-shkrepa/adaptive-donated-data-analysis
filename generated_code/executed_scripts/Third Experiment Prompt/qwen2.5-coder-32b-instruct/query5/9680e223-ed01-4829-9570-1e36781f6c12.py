import os
import csv
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the login activity file
login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to convert timestamp to datetime string
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Check if the login activity file exists
if not os.path.exists(login_activity_path):
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    # Write only the column headers to the CSV file
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Device ID", "Login Time"])
    print("Login activity file not found. Created an empty CSV with headers.")
else:
    # Read the login activity file
    with open(login_activity_path, 'r') as file:
        try:
            login_data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("ValueError: The login activity file is not a valid JSON file.")

    # Check if the expected structure exists in the JSON data
    if "account_history_login_history" not in login_data:
        raise ValueError("ValueError: The login activity file does not contain the expected structure.")

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Write the login activity data to the CSV file
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Device ID", "Login Time"])
        for entry in login_data["account_history_login_history"]:
            device_id = entry["string_map_data"].get("Device ID", {}).get("value", "")
            timestamp = entry["string_map_data"].get("Time", {}).get("timestamp", 0)
            login_time = timestamp_to_datetime(timestamp)
            csv_writer.writerow([device_id, login_time])

    print("CSV file created successfully with login activity data.")