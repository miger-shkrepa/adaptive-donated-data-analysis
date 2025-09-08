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

# Function to extract login times from the notification_of_privacy_policy_updates.json file
def extract_login_times(root_dir):
    login_times = []
    file_path = os.path.join(root_dir, "logged_information", "policy_updates_and_permissions", "notification_of_privacy_policy_updates.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(file_path):
        return login_times
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get("policy_updates_and_permissions_notification_of_privacy_policy_updates", []):
                string_map_data = entry.get("string_map_data", {})
                timestamp_str = string_map_data.get("Impression Time", {}).get("value", "")
                if timestamp_str:
                    try:
                        timestamp = int(timestamp_str)
                        login_time = timestamp_to_datetime(timestamp)
                        login_times.append(("Unknown", login_time))
                    except ValueError as e:
                        print(f"Warning: {e}")
    except (json.JSONDecodeError, IOError) as e:
        raise ValueError(f"ValueError: Error reading or parsing the file {file_path}") from e
    
    return login_times

# Main function to generate the CSV file
def generate_csv(root_dir):
    login_times = extract_login_times(root_dir)
    
    # Define the CSV file path
    csv_file_path = "query_responses/results.csv"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    # Write the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Device ID", "Login Time"])
        csvwriter.writerows(login_times)

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(f"Error: {e}")