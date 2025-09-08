import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_login_info(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store device IDs and login times
        device_ids = []
        login_times = []

        # Iterate over all files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Check if the JSON file contains device information
                    if "devices_devices" in data:
                        # Iterate over all devices in the JSON file
                        for device in data["devices_devices"]:
                            # Check if the device has a "Last Login" entry
                            if "Last Login" in device["string_map_data"]:
                                # Extract the device ID and login time
                                device_id = device["string_map_data"]["User Agent"]["value"]
                                login_time = device["string_map_data"]["Last Login"]["value"]

                                # Convert the login time to the required format
                                try:
                                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    raise ValueError("ValueError: Invalid login time format.")

                                # Add the device ID and login time to the lists
                                device_ids.append(device_id)
                                login_times.append(login_time)

        # Create a CSV file with the device IDs and login times
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(len(device_ids)):
                writer.writerow({'Device ID': device_ids[i], 'Login Time': login_times[i]})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except ValueError as e:
        raise ValueError(f"ValueError: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

get_device_login_info(root_dir)