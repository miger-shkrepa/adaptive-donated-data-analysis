import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def process_devices_data(root_dir):
    devices_file_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
    output_file_path = "query_responses/results.csv"
    
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        if not os.path.exists(devices_file_path):
            with open(output_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return
        
        with open(devices_file_path, 'r') as file:
            data = json.load(file)
        
        devices_devices = data.get("devices_devices", [])
        
        if not devices_devices:
            with open(output_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return
        
        results = []
        for device in devices_devices:
            user_agent = device.get("string_map_data", {}).get("User Agent", {}).get("value", "")
            last_login_timestamp = device.get("string_map_data", {}).get("Last Login", {}).get("timestamp", 0)
            
            if user_agent and last_login_timestamp:
                login_time = datetime.fromtimestamp(last_login_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                results.append([user_agent, login_time])
        
        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(results)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
process_devices_data(root_dir)