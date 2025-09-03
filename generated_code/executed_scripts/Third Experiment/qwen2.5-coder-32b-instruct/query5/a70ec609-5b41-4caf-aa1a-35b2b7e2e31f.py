import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_device_login_times(root_directory):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the devices.json file
        devices_file_path = os.path.join(root_directory, "personal_information", "device_information", "devices.json")
        
        # Check if the devices.json file exists
        if not os.path.exists(devices_file_path):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")
        
        # Read the devices.json file
        with open(devices_file_path, 'r', encoding='utf-8') as file:
            devices_data = json.load(file)
        
        # Check if the expected structure exists in the JSON data
        if 'devices_devices' not in devices_data:
            raise ValueError("ValueError: The devices.json file does not contain the expected structure.")
        
        # Prepare the data for CSV
        device_login_times = []
        for device in devices_data['devices_devices']:
            device_id = device['string_map_data'].get('GerÃ¤te-ID', {}).get('value', '')
            login_time = device['string_map_data'].get('Last Login', {}).get('value', '')
            
            # Convert login time to the required format
            if login_time:
                try:
                    login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    login_time = ''
            
            device_login_times.append((device_id, login_time))
        
        # Write the data to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
            csvwriter.writerows(device_login_times)
    
    except Exception as e:
        # Write only the column headers if an error occurs
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Device ID', 'Login Time'])
        print(f"An error occurred: {e}")

# Call the function to generate the CSV
get_device_login_times(root_dir)