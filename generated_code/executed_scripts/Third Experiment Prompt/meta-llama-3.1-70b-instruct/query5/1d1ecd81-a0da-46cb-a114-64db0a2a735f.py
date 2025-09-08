import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_login_info(root_dir):
    device_login_info = []
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    try:
        with open(devices_file_path, 'r') as devices_file:
            devices_data = json.load(devices_file)
            for device in devices_data["devices_devices"]:
                device_id = device["title"]
                login_time = device["string_map_data"]["Last Login"]["value"]
                login_time = datetime.strptime(login_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                device_login_info.append((device_id, login_time))
    except FileNotFoundError:
        raise FileNotFoundError("Error: The devices.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The devices.json file is not a valid JSON file.")
    except KeyError as e:
        raise ValueError(f"Error: The devices.json file is missing the key '{e.args[0]}'")
    
    return device_login_info

def write_to_csv(device_login_info):
    csv_file_path = "query_responses/results.csv"
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Device ID", "Login Time"])
        for device_id, login_time in device_login_info:
            csv_writer.writerow([device_id, login_time])

def main():
    try:
        device_login_info = get_device_login_info(root_dir)
        write_to_csv(device_login_info)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()