import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def convert_timestamp_to_datetime(timestamp):
    try:
        return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Error: Invalid timestamp value.")

def main():
    devices_file_path = os.path.join(root_dir, "devices.json")
    results = []

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(devices_file_path):
        # Save CSV with only headers if the file is missing
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
        return

    try:
        with open(devices_file_path, 'r') as file:
            devices_data = json.load(file)
        
        for device in devices_data.get('devices_devices', []):
            device_id = device.get('title', 'Unknown')
            login_time_info = device.get('string_map_data', {}).get('Last Login', {})
            login_timestamp = login_time_info.get('timestamp', None)
            
            if login_timestamp:
                login_time = convert_timestamp_to_datetime(login_timestamp)
                results.append([device_id, login_time])
            else:
                results.append([device_id, 'Unknown'])

    except json.JSONDecodeError:
        raise ValueError("Error: The devices.json file is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

    # Write results to CSV
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        writer.writerows(results)

if __name__ == "__main__":
    main()