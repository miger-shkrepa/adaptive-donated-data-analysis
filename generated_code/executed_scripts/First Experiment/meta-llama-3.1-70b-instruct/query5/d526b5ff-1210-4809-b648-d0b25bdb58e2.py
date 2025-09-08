import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    devices = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "devices.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for device in data["devices_devices"]:
                        string_map_data = device["string_map_data"]
                        if "Last Login" in string_map_data:
                            device_id = string_map_data["User Agent"]["value"] if "User Agent" in string_map_data else "Unknown"
                            login_time = string_map_data["Last Login"]["value"]
                            if login_time:
                                try:
                                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    raise ValueError("ValueError: Invalid login time format.")
                            devices.append((device_id, login_time))
    
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for device in devices:
            writer.writerow({'Device ID': device[0], 'Login Time': device[1]})
    
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error: {str(e)}")