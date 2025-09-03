import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Function to parse the login information from the JSON file
def parse_login_info(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            devices = data.get('devices_devices', [])
            login_info = []
            for device in devices:
                string_map_data = device.get('string_map_data', {})
                device_id = string_map_data.get('GerÃ¤te-ID', {}).get('value', 'Unknown')
                login_time = string_map_data.get('Last Login', {}).get('value', 'Unknown')
                if login_time != 'Unknown':
                    login_time = datetime.fromtimestamp(int(login_time) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                login_info.append((device_id, login_time))
            return login_info
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to write the login information to a CSV file
def write_to_csv(login_info):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        writer.writerows(login_info)

# Main function to process the directory and generate the CSV file
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        devices_file = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')
        if not os.path.exists(devices_file):
            # If the devices file does not exist, create a CSV with only the column headers
            write_to_csv([])
            return

        login_info = parse_login_info(devices_file)
        write_to_csv(login_info)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()