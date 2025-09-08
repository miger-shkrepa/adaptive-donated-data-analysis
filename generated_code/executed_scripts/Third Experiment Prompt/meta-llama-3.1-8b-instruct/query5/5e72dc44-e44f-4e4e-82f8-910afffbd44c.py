import csv
import os
import json

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
    for dir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(dir, file)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if 'devices' in data and 'devices_devices' in data['devices']:
                            for device in data['devices']['devices_devices']:
                                if 'string_map_data' in device and 'Last Login' in device['string_map_data']:
                                    login_time = device['string_map_data']['Last Login']['value']
                                    writer.writerow([device['title'], login_time])
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file {file_path}")
                except KeyError:
                    print(f"Error: Missing key in file {file_path}")