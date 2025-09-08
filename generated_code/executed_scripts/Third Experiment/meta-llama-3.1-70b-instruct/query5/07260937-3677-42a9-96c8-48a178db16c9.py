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

        # Iterate through the directory structure
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name == "devices.json":
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        with open(file_path, 'r') as file:
                            # Since we don't have the exact JSON structure, we'll assume it's a list of dictionaries
                            # with 'string_map_data' containing 'Device ID' and 'Last Login' keys
                            import json
                            data = json.load(file)
                            for item in data['devices_devices']:
                                device_id = item['string_map_data'].get('Device ID', {}).get('value')
                                login_time = item['string_map_data'].get('Last Login', {}).get('value')
                                if device_id and login_time:
                                    # Convert login time to desired format
                                    try:
                                        login_time = datetime.strptime(login_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                                        login_time = login_time.strftime('%Y-%m-%d %H:%M:%S')
                                    except ValueError:
                                        # If login time is not in the expected format, skip it
                                        continue
                                    device_ids.append(device_id)
                                    login_times.append(login_time)
                    except Exception as e:
                        raise ValueError("ValueError: Failed to parse devices.json file.") from e

        # Create CSV file with device IDs and login times
        with open('query_responses/results.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Device ID", "Login Time"])
            for device_id, login_time in zip(device_ids, login_times):
                writer.writerow([device_id, login_time])

    except Exception as e:
        # If any error occurs, create a CSV file with only column headers
        with open('query_responses/results.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Device ID", "Login Time"])
        raise

get_device_login_info(root_dir)