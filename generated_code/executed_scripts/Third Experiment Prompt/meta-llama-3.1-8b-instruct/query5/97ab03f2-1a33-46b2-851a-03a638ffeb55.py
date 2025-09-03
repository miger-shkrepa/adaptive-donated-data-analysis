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
        if "device_information" in dirs:
            for filename in os.listdir(os.path.join(root, "device_information")):
                if filename == "devices.json":
                    with open(os.path.join(root, "device_information", filename), 'r') as f:
                        data = json.load(f)
                        for device in data["devices_devices"]:
                            login_time = device["string_map_data"]["Last Login"]["value"]
                            writer.writerow([device["title"], login_time])
        elif "security_and_login_information" in dirs:
            for filename in os.listdir(os.path.join(root, "security_and_login_information")):
                if filename == "last_known_location.json":
                    try:
                        with open(os.path.join(root, "security_and_login_information", filename), 'r') as f:
                            data = json.load(f)
                            for location in data["account_history_imprecise_last_known_location"]:
                                login_time = location["string_map_data"]["Upload-Zeitpunkt"]["value"]
                                writer.writerow(["Unknown", login_time])
                    except FileNotFoundError:
                        pass
                elif filename == "signup_information.json":
                    try:
                        with open(os.path.join(root, "security_and_login_information", filename), 'r') as f:
                            data = json.load(f)
                            for info in data["account_history_registration_info"]:
                                login_time = info["string_map_data"]["Zeit"]["value"]
                                writer.writerow(["Unknown", login_time])
                    except FileNotFoundError:
                        pass