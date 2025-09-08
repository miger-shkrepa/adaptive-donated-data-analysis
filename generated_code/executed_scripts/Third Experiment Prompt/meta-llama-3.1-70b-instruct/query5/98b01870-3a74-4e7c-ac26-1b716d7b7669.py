import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_devices_login_time(root_dir):
    devices_login_time = []
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    try:
        if os.path.exists(devices_file_path):
            with open(devices_file_path, 'r') as devices_file:
                devices_data = json.load(devices_file)
                if "devices_devices" in devices_data:
                    for device in devices_data["devices_devices"]:
                        if "string_map_data" in device:
                            if "Device ID" in device["string_map_data"] and "Last Login" in device["string_map_data"]:
                                device_id = device["string_map_data"]["Device ID"]["value"]
                                login_time = device["string_map_data"]["Last Login"]["value"]
                                login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                                devices_login_time.append([device_id, login_time])
        else:
            raise FileNotFoundError("Error: The devices.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The devices.json file is not a valid JSON file.")
    
    return devices_login_time

def save_to_csv(devices_login_time):
    csv_file_path = "query_responses/results.csv"
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Device ID", "Login Time"])
        csv_writer.writerows(devices_login_time)

def main():
    try:
        devices_login_time = get_devices_login_time(root_dir)
        save_to_csv(devices_login_time)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()