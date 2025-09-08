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
            # Open the devices.json file
            with open(devices_file_path, 'r') as file:
                # Load the JSON data
                import json
                data = json.load(file)

                # Extract the device information
                for device in data.get("devices_devices", []):
                    device_id = device.get("string_map_data", {}).get("User Agent", {}).get("value")
                    login_time = device.get("string_map_data", {}).get("Last Login", {}).get("value")

                    # Convert the login time to the required format
                    if login_time:
                        try:
                            login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            login_time = None

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

    except Exception as e:
        # Handle any exceptions
        raise Exception(f"Error: {str(e)}")

get_login_devices(root_dir)