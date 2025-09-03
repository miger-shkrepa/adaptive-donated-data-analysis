import os
import csv
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
                # Since the structure of the JSON file is not provided, we assume it's a simple JSON object
                # In a real-world scenario, you would use a JSON parser to parse the file content
                # For simplicity, we will assume the file content is a string representation of a Python dictionary
                import json
                devices_data = json.load(file)

                # Iterate over the devices
                for device in devices_data.get("devices_devices", []):
                    # Extract the device ID and login time
                    device_id = device.get("string_map_data", {}).get("Device ID", {}).get("value")
                    login_time_timestamp = device.get("string_map_data", {}).get("Last Login", {}).get("timestamp")

                    # Convert the login time timestamp to a datetime object
                    if login_time_timestamp:
                        login_time = datetime.fromtimestamp(int(login_time_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        login_time = ""

                    # Add the device information to the list
                    devices.append((device_id, login_time))

        # Save the device information to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the device information
            for device in devices:
                writer.writerow({'Device ID': device[0], 'Login Time': device[1]})

    except FileNotFoundError as e:
        # If the root directory or the devices.json file does not exist, create a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise e

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_login_devices(root_dir)