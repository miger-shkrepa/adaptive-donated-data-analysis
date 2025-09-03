import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Iterate over all files in the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "login_history.json":
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for login in data["login_history"]:
                        device_id = login["string_map_data"]["Device ID"]["value"]
                        login_time = datetime.fromtimestamp(login["string_map_data"]["Login Time"]["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
                        results.append([device_id, login_time])
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {filepath} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {filepath} is not a valid JSON file.")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)