import csv
import os
import json

root_dir = "root_dir"

def get_device_login_times(root_dir):
    device_login_times = {}
    for dir_name in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, dir_name)
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if file_name.endswith('.json'):
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            if 'story_activities_story_likes' in data['structure']:
                                for item in data['structure']['story_activities_story_likes']:
                                    if 'string_list_data' in item:
                                        for item2 in item['string_list_data']:
                                            if 'timestamp' in item2:
                                                timestamp = item2['timestamp']
                                                device_id = dir_name
                                                if device_id not in device_login_times:
                                                    device_login_times[device_id] = []
                                                device_login_times[device_id].append(timestamp)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {file_path}: {e}")
    return device_login_times

def write_device_login_times_to_csv(device_login_times):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        for device_id, login_times in device_login_times.items():
            for timestamp in login_times:
                writer.writerow([device_id, timestamp])

try:
    device_login_times = get_device_login_times(root_dir)
    write_device_login_times_to_csv(device_login_times)
except FileNotFoundError as e:
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    raise ValueError("ValueError: An error occurred while processing the data: " + str(e))