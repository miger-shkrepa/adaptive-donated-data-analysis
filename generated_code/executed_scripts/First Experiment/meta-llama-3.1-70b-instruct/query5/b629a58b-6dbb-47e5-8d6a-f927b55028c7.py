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

        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Check if the file is the devices.json file
                    if filename == "devices.json":
                        # Iterate over the devices
                        for device in data["devices_devices"]:
                            # Get the device ID and login time
                            device_id = device["string_map_data"]["User Agent"]["value"]
                            login_time = device["string_map_data"]["Last Login"]["value"]

                            # Convert the login time to the required format
                            login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')

                            # Add the device ID and login time to the lists
                            device_ids.append(device_id)
                            login_times.append(login_time)

        # Create a CSV writer
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header
            writer.writerow(["Device ID", "Login Time"])

            # Write the device IDs and login times
            for i in range(len(device_ids)):
                writer.writerow([device_ids[i], login_times[i]])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

get_device_login_info(root_dir)