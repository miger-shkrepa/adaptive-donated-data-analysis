import os
import json
from datetime import datetime
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

devices_login_times = []

try:
    with open(os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")) as f:
        data = json.load(f)
        for login in data["account_history_login_history"]:
            device_id = login["string_map_data"].get("Cookie Name", {}).get("value", "N/A")
            login_time = login["string_map_data"].get("Time", {}).get("value", "N/A")
            if login_time != "N/A" and login_time != "":
                login_time = datetime.fromtimestamp(int(login_time)).strftime('%Y-%m-%d %H:%M:%S')
            devices_login_times.append((device_id, login_time))
except FileNotFoundError:
    pass

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(devices_login_times)