import os
import json
import csv

root_dir = "root_dir"

def get_devices_login_time(root_dir):
    devices_login_time = []
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    try:
        if not os.path.exists(devices_file_path):
            return devices_login_time
        
        with open(devices_file_path, 'r') as devices_file:
            devices_data = json.load(devices_file)
            if "devices_devices" not in devices_data:
                return devices_login_time
            
            for device in devices_data["devices_devices"]:
                if "string_map_data" not in device:
                    continue
                
                device_id = device["string_map_data"].get("Device ID", {}).get("value")
                login_time = device["string_map_data"].get("Last Login", {}).get("value")
                
                if device_id and login_time:
                    devices_login_time.append((device_id, login_time))
    except json.JSONDecodeError:
        raise ValueError("Error: The devices.json file is not a valid JSON file.")
    
    return devices_login_time

def save_to_csv(devices_login_time):
    csv_file_path = "query_responses/results.csv"
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Device ID", "Login Time"])
        for device_id, login_time in devices_login_time:
            csv_writer.writerow([device_id, login_time])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        devices_login_time = get_devices_login_time(root_dir)
        save_to_csv(devices_login_time)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()