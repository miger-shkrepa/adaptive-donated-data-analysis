import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Traverse the directory structure
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".json"):
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'structure' in data and 'messages' in data['structure']:
                        for message in data['structure']['messages']:
                            if 'sender_name' in message and 'timestamp_ms' in message:
                                device_id = message['sender_name']
                                login_time = datetime.fromtimestamp(int(message['timestamp_ms']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                results.append([device_id, login_time])

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Device ID', 'Login Time'])
    writer.writerows(results)