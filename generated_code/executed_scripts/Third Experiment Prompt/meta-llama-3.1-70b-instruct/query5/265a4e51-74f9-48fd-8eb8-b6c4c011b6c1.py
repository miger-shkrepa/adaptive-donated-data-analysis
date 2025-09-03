import os
import csv
import json

root_dir = "root_dir"

def get_device_login_info(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize output list
        output = []

        # Iterate through directories
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Check if 'devices.json' file exists
            if 'devices.json' in filenames:
                devices_file_path = os.path.join(dirpath, 'devices.json')

                # Open and read 'devices.json' file
                with open(devices_file_path, 'r') as file:
                    devices_data = json.load(file)

                    # Iterate through devices data
                    for device in devices_data.get('devices_devices', []):
                        # Extract device ID and login time
                        string_map_data = device.get('string_map_data', {})
                        device_id = string_map_data.get('Geräte-ID', {}).get('value')
                        login_time = string_map_data.get('Last Login', {}).get('value')

                        # Append to output list if both device ID and login time are available
                        if device_id and login_time:
                            output.append([device_id, login_time])

        # Write output to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])  # Write header
            writer.writerows(output)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_device_login_info(root_dir)