import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

def process_devices_login_data(root_directory):
    devices_login_data = []
    devices_json_path = os.path.join(root_directory, "personal_information", "device_information", "devices.json")
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(devices_json_path):
        return devices_login_data

    try:
        with open(devices_json_path, 'r', encoding='utf-8') as file:
            devices_data = json.load(file)
            for device in devices_data.get("devices_devices", []):
                string_map_data = device.get("string_map_data", {})
                device_id = string_map_data.get("Device ID", {}).get("value")
                last_login_timestamp = string_map_data.get("Last Login", {}).get("timestamp")
                if device_id and last_login_timestamp:
                    login_time = parse_timestamp(last_login_timestamp)
                    devices_login_data.append({"Device ID": device_id, "Login Time": login_time})
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

    return devices_login_data

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

try:
    devices_login_data = process_devices_login_data(root_dir)
    write_to_csv(devices_login_data, 'query_responses/results.csv')
except Exception as e:
    print(str(e))
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()