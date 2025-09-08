import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse the JSON files and extract the required data
def extract_device_info(root_dir):
    device_info = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the paths to the relevant JSON files
    devices_json_path = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')
    login_activity_json_path = os.path.join(root_dir, 'security_and_login_information', 'login_and_profile_creation', 'login_activity.json')

    # Check if the devices.json file exists
    if not os.path.exists(devices_json_path):
        raise FileNotFoundError("Error: The devices.json file does not exist.")

    # Check if the login_activity.json file exists
    if not os.path.exists(login_activity_json_path):
        raise FileNotFoundError("Error: The login_activity.json file does not exist.")

    # Load the devices.json file
    with open(devices_json_path, 'r') as devices_file:
        devices_data = json.load(devices_file)

    # Load the login_activity.json file
    with open(login_activity_json_path, 'r') as login_file:
        login_data = json.load(login_file)

    # Extract device IDs and login times
    for device in devices_data.get('devices_devices', []):
        device_id = device['string_map_data'].get('Device ID', {}).get('value', '')
        last_login_timestamp = device['string_map_data'].get('Last Login', {}).get('timestamp', 0)

        if device_id and last_login_timestamp:
            # Convert the timestamp to a datetime object
            last_login_time = datetime.fromtimestamp(last_login_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            device_info.append((device_id, last_login_time))

    return device_info

# Function to write the extracted data to a CSV file
def write_to_csv(device_info, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Device ID', 'Login Time'])
        csvwriter.writerows(device_info)

# Main function to execute the script
def main():
    try:
        device_info = extract_device_info(root_dir)
        write_to_csv(device_info, output_csv)
        print(f"Data successfully written to {output_csv}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()