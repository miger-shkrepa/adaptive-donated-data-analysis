import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_device_login_times(root_dir):
    device_login_times = []
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)
            if os.path.isdir(dir_path):
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)
                    if os.path.isfile(file_path) and file_name.endswith(".json"):
                        try:
                            with open(file_path, 'r') as file:
                                # Since the exact structure of the JSON files is not provided,
                                # we assume that the 'timestamp_ms' field represents the login time
                                # and the 'sender_name' field represents the device ID.
                                # However, based on the given directory structure, 
                                # it seems that the 'timestamp_ms' field is the only relevant field.
                                # Therefore, we will use the directory name as the device ID.
                                for line in file:
                                    # The JSON files are not in a standard format, so we cannot use the json library.
                                    # We will assume that each line represents a single login event.
                                    if '"timestamp_ms"' in line:
                                        timestamp_ms = int(line.split('"timestamp_ms":')[1].split(',')[0])
                                        login_time = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                        device_id = dir_name
                                        device_login_times.append((device_id, login_time))
                        except Exception as e:
                            raise ValueError("ValueError: Failed to parse JSON file: " + str(e))
    except Exception as e:
        raise ValueError("ValueError: Failed to process directory: " + str(e))
    
    return device_login_times

def save_to_csv(device_login_times):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            for device_id, login_time in device_login_times:
                writer.writerow([device_id, login_time])
    except Exception as e:
        raise ValueError("ValueError: Failed to save to CSV file: " + str(e))

def main():
    try:
        device_login_times = get_device_login_times(root_dir)
        if not device_login_times:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Device ID", "Login Time"])
        else:
            save_to_csv(device_login_times)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()