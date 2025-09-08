import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_data(root_directory):
    device_logins = []

    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        for dirpath, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                if filename == "device_logins.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if "device_logins" in data:
                            for login in data["device_logins"]:
                                if "device_id" in login and "login_time" in login:
                                    try:
                                        login_time = datetime.fromtimestamp(login["login_time"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                        device_logins.append({"Device ID": login["device_id"], "Login Time": login_time})
                                    except ValueError:
                                        raise ValueError("Error: Invalid timestamp value in device_logins.json.")
                                else:
                                    raise ValueError("Error: Missing 'device_id' or 'login_time' in device_logins.json.")
                        else:
                            raise ValueError("Error: 'device_logins' key not found in device_logins.json.")
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)

    return device_logins

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

device_logins = process_data(root_dir)
write_to_csv(device_logins)