import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def extract_device_info(root_dir):
    try:
        # Define the path to the devices.json file
        devices_file_path = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')

        # Check if the file exists
        if not os.path.exists(devices_file_path):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")

        # Read the JSON file
        with open(devices_file_path, 'r') as file:
            data = json.load(file)

        # Extract the required information
        device_info = []
        for device in data.get('devices_devices', []):
            user_agent = device.get('string_map_data', {}).get('User Agent', {}).get('value', '')
            last_login_timestamp = device.get('string_map_data', {}).get('Last Login', {}).get('timestamp', 0)

            # Convert timestamp to datetime
            try:
                login_time = datetime.fromtimestamp(last_login_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                login_time = 'Invalid Timestamp'

            device_info.append((user_agent, login_time))

        # Write the results to a CSV file
        output_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
            csvwriter.writerows(device_info)

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        # Create an empty CSV file with headers
        output_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])

    except ValueError as ve:
        print(f"ValueError: {ve}")

    except Exception as e:
        print(f"Error: {e}")

# Execute the function
extract_device_info(root_dir)