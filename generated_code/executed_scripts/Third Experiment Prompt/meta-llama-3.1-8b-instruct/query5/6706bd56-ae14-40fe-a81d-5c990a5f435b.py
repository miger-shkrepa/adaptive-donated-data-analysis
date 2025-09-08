import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Device ID", "Login Time"])

    # Iterate over the directory structure
    for root, dirs, files in os.walk(root_dir):
        if "security_and_login_information" in dirs:
            security_dir = os.path.join(root, "security_and_login_information")
            if os.path.exists(security_dir):
                for subroot, subdirs, subfiles in os.walk(security_dir):
                    if "login_and_account_creation" in subdirs:
                        login_dir = os.path.join(subroot, "login_and_account_creation")
                        if os.path.exists(login_dir):
                            for filename in os.listdir(login_dir):
                                if filename.endswith(".json"):
                                    file_path = os.path.join(login_dir, filename)
                                    try:
                                        with open(file_path, 'r') as json_file:
                                            data = json.load(json_file)
                                            for item in data.get("account_history_login_history", []):
                                                device_id = item.get("string_map_data", {}).get("Device")
                                                login_time = item.get("string_map_data", {}).get("Time")
                                                if device_id and login_time:
                                                    writer.writerow([device_id, login_time])
                                    except json.JSONDecodeError as e:
                                        print(f"Error parsing JSON file: {e}")