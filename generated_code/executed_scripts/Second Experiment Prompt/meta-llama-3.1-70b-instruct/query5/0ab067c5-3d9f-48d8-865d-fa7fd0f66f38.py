import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the list to store device information
        devices = []

        # Define the path to the devices.json file
        devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

        # Check if the devices.json file exists
        if os.path.exists(devices_file_path):
            # Open the devices.json file and read its content
            with open(devices_file_path, 'r') as file:
                # Load the JSON content
                content = json.load(file)
                # Extract the device information
                for device_info in content['devices_devices']:
                    # Extract the device ID and login time
                    device_id = None
                    login_time = None
                    if 'string_map_data' in device_info:
                        for key, value in device_info['string_map_data'].items():
                            if key == 'Device ID':
                                device_id = value['value']
                            elif key == 'Last Login':
                                login_time = value['value']
                                # Convert the login time to the required format
                                if login_time:
                                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                    # Add the device information to the list
                    if device_id and login_time:
                        devices.append((device_id, login_time))

        # Save the device information to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in devices:
                writer.writerow({'Device ID': device[0], 'Login Time': device[1]})

    except FileNotFoundError as e:
        # If the root directory or the devices.json file does not exist, save a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise FileNotFoundError("FileNotFoundError: The root directory or the devices.json file does not exist.")

    except json.JSONDecodeError as e:
        # If the JSON file is invalid, save a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise ValueError("Error: The devices.json file is not a valid JSON file.")

    except Exception as e:
        raise ValueError("Error: An unexpected error occurred - " + str(e))

get_login_devices(root_dir)