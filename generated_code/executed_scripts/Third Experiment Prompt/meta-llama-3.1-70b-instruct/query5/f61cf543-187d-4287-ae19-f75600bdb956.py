import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_device_login_info(root_dir):
    device_login_info = []
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    
    try:
        with open(devices_file_path, 'r') as devices_file:
            devices_data = json.load(devices_file)
            devices = devices_data.get("devices_devices", [])
            
            for device in devices:
                device_id = device.get("string_map_data", {}).get("Device ID", {}).get("value")
                login_time = device.get("string_map_data", {}).get("Last Login", {}).get("value")
                
                if device_id and login_time:
                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                    device_login_info.append((device_id, login_time))
                    
    except FileNotFoundError:
        raise FileNotFoundError("Error: The devices.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The devices.json file is not a valid JSON file.")
        
    return device_login_info

def save_to_csv(device_login_info):
    csv_file_path = "query_responses/results.csv"
    csv_columns = ["Device ID", "Login Time"]
    
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_columns)
            csv_writer.writerows(device_login_info)
            
    except Exception as e:
        raise Exception(f"Error: Failed to save data to CSV file. {str(e)}")

def main():
    device_login_info = get_device_login_info(root_dir)
    save_to_csv(device_login_info)

if __name__ == "__main__":
    main()