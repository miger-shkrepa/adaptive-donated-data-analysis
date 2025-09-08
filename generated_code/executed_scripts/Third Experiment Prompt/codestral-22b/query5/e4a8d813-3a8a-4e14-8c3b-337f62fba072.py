import os
import json
from datetime import datetime
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

login_activity_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "login_activity.json")

if os.path.exists(login_activity_path):
    with open(login_activity_path, 'r') as f:
        data = json.load(f)
        for login in data.get("account_history_login_history", []):
            device_id = login["string_map_data"].get("Cookie Name", {}).get("value", "")
            login_time_str = login["string_map_data"].get("Time", {}).get("value", "")
            try:
                login_time = datetime.fromtimestamp(int(login_time_str)).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                login_time = ""
            results.append((device_id, login_time))

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)