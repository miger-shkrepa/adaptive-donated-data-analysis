import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_devices_login_time(root_dir):
    devices_login_time = []
    try:
        devices_json_path = os.path.join(root_dir, "devices.json")
        if not os.path.exists(devices_json_path):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")
        
        with open(devices_json_path, 'r') as file:
            devices_data = eval(file.read())
            for device in devices_data["devices_devices"]:
                device_id = device["title"]
                login_time = device["string_map_data"]["Last Login"]["value"]
                login_time_timestamp = device["string_map_data"]["Last Login"]["timestamp"]
                login_time_datetime = datetime.fromtimestamp(login_time_timestamp)
                login_time_formatted = login_time_datetime.strftime('%Y-%m-%d %H:%M:%S')
                devices_login_time.append((device_id, login_time_formatted))
        
        login_activity_json_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")
        if os.path.exists(login_activity_json_path):
            with open(login_activity_json_path, 'r') as file:
                login_activity_data = eval(file.read())
                for login_activity in login_activity_data["account_history_login_history"]:
                    device_id = login_activity["string_map_data"]["User Agent"]["value"]
                    login_time = login_activity["string_map_data"]["Time"]["value"]
                    login_time_timestamp = login_activity["string_map_data"]["Time"]["timestamp"]
                    login_time_datetime = datetime.fromtimestamp(login_time_timestamp)
                    login_time_formatted = login_time_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    devices_login_time.append((device_id, login_time_formatted))
        
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    
    return devices_login_time

def save_to_csv(devices_login_time):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            for device in devices_login_time:
                writer.writerow(device)
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        devices_login_time = get_devices_login_time(root_dir)
        if not devices_login_time:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Device ID", "Login Time"])
        else:
            save_to_csv(devices_login_time)
    except Exception as e:
        if "FileNotFoundError" in str(e):
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Device ID", "Login Time"])
        else:
            raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()