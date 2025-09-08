import os
import csv
import json
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to convert timestamp to the required format
def convert_timestamp_to_datetime(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (OSError, OverflowError, ValueError) as e:
        raise ValueError(f"ValueError: Failed to convert timestamp {timestamp} to datetime. Reason: {e}")

# Function to process the login activity file
def process_login_activity_file(file_path):
    devices_and_times = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'account_history_login_history' in data:
                for entry in data['account_history_login_history']:
                    if 'string_map_data' in entry:
                        string_map_data = entry['string_map_data']
                        device_id = string_map_data.get('Device', {}).get('value', '')
                        login_time = string_map_data.get('Time', {}).get('timestamp', None)
                        if login_time is not None:
                            login_time_formatted = convert_timestamp_to_datetime(login_time)
                            devices_and_times.append((device_id, login_time_formatted))
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Failed to decode JSON from file {file_path}. Reason: {e}")
    return devices_and_times

# Main function to execute the query
def main():
    # Define the path to the login activity file
    login_activity_file_path = os.path.join(root_dir, 'security_and_login_information', 'login_and_profile_creation', 'login_activity.json')
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the login activity file exists
    if not os.path.exists(login_activity_file_path):
        # If the file does not exist, create an empty CSV with headers
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
        return
    
    # Process the login activity file
    devices_and_times = process_login_activity_file(login_activity_file_path)
    
    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        writer.writerows(devices_and_times)

# Execute the main function
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")