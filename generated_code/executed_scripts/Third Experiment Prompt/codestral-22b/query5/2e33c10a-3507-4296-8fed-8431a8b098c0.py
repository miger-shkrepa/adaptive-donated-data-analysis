import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

login_history_path = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "login_activity.json")

if os.path.exists(login_history_path):
    with open(login_history_path, 'r') as f:
        data = json.load(f)
        for login in data["account_history_login_history"]:
            device_id = login["string_map_data"]["Name des Cookies"]["value"]
            login_time = datetime.fromtimestamp(login["string_map_data"]["Zeit"]["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
            results.append([device_id, login_time])

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)