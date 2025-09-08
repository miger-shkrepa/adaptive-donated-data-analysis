import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def extract_login_info(json_data):
    login_info = []
    for device in json_data['devices_devices']:
        for key, value in device['string_map_data'].items():
            if key == 'Last Login':
                login_info.append({
                    'Device ID': device['title'],
                    'Login Time': datetime.fromtimestamp(value['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                })
    return login_info

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Device ID', 'Login Time'])
        writer.writeheader()
        writer.writerows(data)

def main():
    try:
        os.chdir(root_dir)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    for file in os.listdir():
        if file.endswith('.json'):
            json_data = load_json_file(file)
            login_info = extract_login_info(json_data)
            save_to_csv(login_info, 'query_responses/results.csv')

if __name__ == "__main__":
    main()