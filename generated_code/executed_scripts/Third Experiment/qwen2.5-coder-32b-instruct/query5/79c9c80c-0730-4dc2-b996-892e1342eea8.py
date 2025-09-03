import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_login_times(root_directory):
    device_login_times = []

    try:
        devices_file_path = os.path.join(root_directory, "personal_information", "device_information", "devices.json")
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        if not os.path.exists(devices_file_path):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")
        
        with open(devices_file_path, 'r', encoding='utf-8') as file:
            devices_data = json.load(file)
        
        if 'devices_devices' not in devices_data:
            raise ValueError("ValueError: The devices.json file does not contain the expected structure.")
        
        for device in devices_data['devices_devices']:
            device_id = device['string_map_data'].get('User Agent', {}).get('value', '')
            login_time = device['string_map_data'].get('Last Login', {}).get('value', '')
            
            try:
                login_time_formatted = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                login_time_formatted = ''
            
            device_login_times.append((device_id, login_time_formatted))
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve_error:
        print(ve_error)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
    
    return device_login_times

def save_to_csv(data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Device ID', 'Login Time'])
            writer.writerows(data)
    except Exception as e:
        print(f"Error: Failed to write to CSV - {str(e)}")

device_login_times = get_device_login_times(root_dir)
save_to_csv(device_login_times, 'query_responses/results.csv')