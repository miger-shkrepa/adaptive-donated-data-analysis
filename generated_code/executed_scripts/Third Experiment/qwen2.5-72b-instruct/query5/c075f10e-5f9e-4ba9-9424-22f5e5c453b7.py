import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_device_information(root_dir):
    device_info_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    if not os.path.exists(device_info_path):
        raise FileNotFoundError("FileNotFoundError: The device information file does not exist.")
    
    try:
        with open(device_info_path, 'r') as file:
            device_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from device information file.")
    
    devices = device_data.get("devices_devices", [])
    device_logins = []
    
    for device in devices:
        string_map_data = device.get("string_map_data", {})
        last_login = string_map_data.get("Last Login", {}).get("value")
        if last_login:
            try:
                login_time = datetime.fromtimestamp(int(last_login) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                device_logins.append({"Device ID": device.get("title", "Unknown"), "Login Time": login_time})
            except ValueError:
                raise ValueError("Error: Invalid timestamp in device login data.")
    
    return device_logins

def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except IOError:
        raise IOError("Error: Failed to write to the output CSV file.")

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        device_logins = process_device_information(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(device_logins, output_path)
    except Exception as e:
        print(e)