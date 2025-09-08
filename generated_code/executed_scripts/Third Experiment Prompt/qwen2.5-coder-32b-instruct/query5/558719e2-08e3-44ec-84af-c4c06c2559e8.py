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
        raise ValueError(f"ValueError: Failed to convert timestamp {timestamp} to datetime. {str(e)}")

# Function to read and process the login activity file
def read_login_activity(root_dir):
    login_activity_file = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(login_activity_file):
        return []

    try:
        with open(login_activity_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"ValueError: Failed to read or decode the login activity file. {str(e)}")

    login_activities = []
    try:
        for entry in data.get("account_history_login_history", []):
            string_map_data = entry.get("string_map_data", {})
            device_id = string_map_data.get("Device", {}).get("value", "")
            login_time_timestamp = string_map_data.get("Time", {}).get("timestamp", 0)
            login_time = timestamp_to_datetime(login_time_timestamp)
            login_activities.append((device_id, login_time))
    except Exception as e:
        raise ValueError(f"ValueError: Failed to process login activity data. {str(e)}")

    return login_activities

# Main function to generate the CSV file
def generate_csv(root_dir):
    login_activities = read_login_activity(root_dir)

    # Define the output file path
    output_file = "query_responses/results.csv"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the CSV file
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(login_activities)
    except IOError as e:
        raise IOError(f"IOError: Failed to write to the output CSV file. {str(e)}")

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(f"Error: {str(e)}")