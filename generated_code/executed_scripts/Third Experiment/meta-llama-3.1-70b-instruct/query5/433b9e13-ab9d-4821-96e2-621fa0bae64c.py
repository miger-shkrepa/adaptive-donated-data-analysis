import os
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

        # Iterate over the directory structure
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if the file is 'devices.json'
                if file_name == 'devices.json':
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and read the 'devices.json' file
                        with open(file_path, 'r') as file:
                            # Since the actual JSON data is not provided, we assume it's in the correct format
                            # and contains the required information
                            data = eval(file.read())
                            for device in data['devices_devices']:
                                device_ids.append(device['string_map_data']['User Agent'])
                                # Convert timestamp to datetime object and then to string in the required format
                                timestamp = device['string_map_data']['Last Login']['timestamp']
                                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                login_times.append(login_time)
                    except Exception as e:
                        raise ValueError("ValueError: Failed to parse 'devices.json' file. " + str(e))

        # Check if any device login information was found
        if not device_ids or not login_times:
            # If not, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Device ID', 'Login Time'])
        else:
            # If device login information was found, write it to the CSV file
            with open('query_responses/results.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Device ID', 'Login Time'])
                for device_id, login_time in zip(device_ids, login_times):
                    csv_writer.writerow([device_id, login_time])

    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the directory structure. " + str(e))

get_device_login_info(root_dir)