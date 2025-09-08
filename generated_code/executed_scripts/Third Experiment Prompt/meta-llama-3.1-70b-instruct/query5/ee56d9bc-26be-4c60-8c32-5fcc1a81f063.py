import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_info(root_dir):
    device_info_path = os.path.join(root_dir, "personal_information", "device_information")
    if not os.path.exists(device_info_path):
        raise FileNotFoundError("Error: Device information directory not found.")
    
    device_info_files = os.listdir(device_info_path)
    device_info = []
    for file in device_info_files:
        file_path = os.path.join(device_info_path, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    device_id = data.get("device_id")
                    login_time = data.get("login_time")
                    if device_id and login_time:
                        login_time = datetime.fromtimestamp(login_time).strftime("%Y-%m-%d %H:%M:%S")
                        device_info.append((device_id, login_time))
                except json.JSONDecodeError:
                    raise ValueError("Error: Invalid JSON file.")
    
    return device_info

def write_csv(device_info):
    csv_path = "query_responses/results.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Device ID", "Login Time"])
        for row in device_info:
            writer.writerow(row)

try:
    device_info = get_device_info(root_dir)
    if not device_info:
        with open("query_responses/results.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Device ID", "Login Time"])
    else:
        write_csv(device_info)
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Device ID", "Login Time"])
except ValueError as e:
    print(e)
    with open("query_responses/results.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Device ID", "Login Time"])