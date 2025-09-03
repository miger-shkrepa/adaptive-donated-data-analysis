import os
import json
from datetime import datetime
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

account_changes_file = os.path.join(root_dir, "security_and_login_information", "login_and_account_creation", "signup_information.json")

if os.path.exists(account_changes_file):
    with open(account_changes_file, 'r') as f:
        data = json.load(f)
        for change in data["account_history_registration_info"]:
            change_date = datetime.fromtimestamp(change["string_map_data"]["Zeit"]["timestamp"]).strftime('%Y-%m-%d')
            for key, value in change["string_map_data"].items():
                if key != "Zeit":
                    results.append([key, value["value"], change_date])

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(results)