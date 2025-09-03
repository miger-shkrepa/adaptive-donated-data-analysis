import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_login_info(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store device IDs and login times
        device_ids = []
        login_times = []

        # Iterate over all files in the root directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if the file is 'devices.json'
                if file_name == 'devices.json':
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and read the 'devices.json' file
                        with open(file_path, 'r') as file:
                            # Since the exact structure of 'devices.json' is not provided, 
                            # we assume it's a list of dictionaries with 'Device ID' and 'Last Login' keys
                            import json
                            data = json.load(file)
                            for item in data['devices_devices']:
                                device_id = item['string_map_data'].get('Device ID', {}).get('value')
                                login_time = item['string_map_data'].get('Last Login', {}).get('value')
                                if device_id and login_time:
                                    # Convert login time to 'YYYY-MM-DD HH:MM:SS' format
                                    try:
                                        login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                                    except ValueError:
                                        # If the conversion fails, skip this login time
                                        continue
                                    device_ids.append(device_id)
                                    login_times.append(login_time)
                    except Exception as e:
                        # If there's an error reading or parsing the file, raise a ValueError
                        raise ValueError("ValueError: Error reading or parsing 'devices.json' file: " + str(e))

        # Create the output CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device_id, login_time in zip(device_ids, login_times):
                writer.writerow({'Device ID': device_id, 'Login Time': login_time})

    except Exception as e:
        # If there's an error, raise a ValueError with the error message
        raise ValueError("ValueError: " + str(e))

get_device_login_info(root_dir)