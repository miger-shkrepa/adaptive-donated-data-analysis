import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to convert timestamp to datetime string
def timestamp_to_datetime(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (OSError, OverflowError, ValueError) as e:
        raise ValueError(f"ValueError: Invalid timestamp value - {timestamp}") from e

# Function to read and process the login activity file
def read_login_activity(root_dir):
    login_activity_file_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(login_activity_file_path):
        return []

    try:
        with open(login_activity_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"ValueError: Error reading or decoding the login activity file - {login_activity_file_path}") from e

    login_activities = []
    try:
        for entry in data.get("account_history_login_history", []):
            string_map_data = entry.get("string_map_data", {})
            device_id = string_map_data.get("Device", {}).get("value", "")
            login_time_timestamp = string_map_data.get("Time", {}).get("timestamp", 0)
            login_time = timestamp_to_datetime(login_time_timestamp)
            login_activities.append((device_id, login_time))
    except Exception as e:
        raise ValueError(f"ValueError: Error processing login activity data - {login_activity_file_path}") from e

    return login_activities

# Main function to generate the CSV file
def generate_csv(root_dir):
    login_activities = read_login_activity(root_dir)

    # Define the output file path
    output_file_path = "query_responses/results.csv"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the CSV file
    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(login_activities)
    except IOError as e:
        raise IOError(f"IOError: Error writing to the output CSV file - {output_file_path}") from e

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(f"Error: {e}")