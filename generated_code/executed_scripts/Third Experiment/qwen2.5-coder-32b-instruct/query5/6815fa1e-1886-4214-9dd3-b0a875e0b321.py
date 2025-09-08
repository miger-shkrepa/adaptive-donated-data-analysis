import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_device_login_times(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the devices.json file
        devices_json_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")
        
        # Check if the devices.json file exists
        if not os.path.exists(devices_json_path):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")
        
        # Read the devices.json file
        with open(devices_json_path, 'r') as file:
            devices_data = json.load(file)
        
        # Prepare the data for CSV
        device_login_times = []
        for device in devices_data.get('devices_devices', []):
            device_id = device['string_map_data'].get('Device ID', {}).get('value', '')
            login_time = device['string_map_data'].get('Last Login', {}).get('value', '')
            
            # Convert login time to the required format
            try:
                login_time_formatted = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, OSError):
                login_time_formatted = '0'
            
            device_login_times.append((device_id, login_time_formatted))
        
        # Write the data to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
            csvwriter.writerows(device_login_times)
    
    except Exception as e:
        # Write only the column headers if an error occurs
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
        print(f"Error: {e}")

# Call the function to generate the CSV
get_device_login_times(root_dir)