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
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        login_activity_path = os.path.join(root_dir, "your_account_activity", "login_activity.json")
        
        if not os.path.exists(login_activity_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
            return
        
        with open(login_activity_path, 'r') as file:
            data = json.load(file)
        
        login_history = data.get('account_history_login_history', [])
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            
            for entry in login_history:
                string_map_data = entry.get('string_map_data', {})
                device = string_map_data.get('Device', {}).get('value', '')
                timestamp = string_map_data.get('Time', {}).get('timestamp', '')
                
                if device and timestamp:
                    login_time = convert_timestamp_to_datetime(timestamp)
                    writer.writerow([device, login_time])
                elif device:
                    writer.writerow([device, ''])
                elif timestamp:
                    login_time = convert_timestamp_to_datetime(timestamp)
                    writer.writerow(['', login_time])

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":
    main()