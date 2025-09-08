import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store device IDs and login times
        device_ids = []
        login_times = []

        # Iterate through the directory structure
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file == "login_activity.json":
                    # Open and read the login activity JSON file
                    with open(os.path.join(root, file), 'r') as f:
                        # Since we don't have the exact JSON structure, we'll assume it's a list of login activities
                        # and each activity has a 'Device' and 'Time' key
                        import json
                        data = json.load(f)
                        for activity in data['account_history_login_history']:
                            device_id = activity['string_map_data'].get('Device', {}).get('value')
                            login_time = activity['string_map_data'].get('Time', {}).get('value')
                            if device_id and login_time:
                                # Convert login time to the required format
                                try:
                                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    # If the time is not in the correct format, skip this login activity
                                    continue
                                device_ids.append(device_id)
                                login_times.append(login_time)

                elif file == "signup_details.json":
                    # Open and read the signup details JSON file
                    with open(os.path.join(root, file), 'r') as f:
                        # Since we don't have the exact JSON structure, we'll assume it's a list of signup details
                        # and each detail has a 'Device' and 'Time' key
                        import json
                        data = json.load(f)
                        for detail in data['account_history_registration_info']:
                            device_id = detail['string_map_data'].get('Device', {}).get('value')
                            login_time = detail['string_map_data'].get('Time', {}).get('value')
                            if device_id and login_time:
                                # Convert login time to the required format
                                try:
                                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    # If the time is not in the correct format, skip this login activity
                                    continue
                                device_ids.append(device_id)
                                login_times.append(login_time)

        # Check if we have any device IDs and login times
        if not device_ids or not login_times:
            # If not, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Device ID', 'Login Time']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        else:
            # If we do, write the device IDs and login times to the CSV file
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Device ID', 'Login Time']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for device_id, login_time in zip(device_ids, login_times):
                    writer.writerow({'Device ID': device_id, 'Login Time': login_time})

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_login_devices(root_dir)