import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the changes
changes = []

# Iterate over the 'messages' directory
messages_dir = os.path.join(root_dir, "messages")
if os.path.exists(messages_dir):
    for subdir in os.listdir(messages_dir):
        subdir_path = os.path.join(messages_dir, subdir)
        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                if file.endswith(".json"):
                    file_path = os.path.join(subdir_path, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'structure' in data and 'messages' in data['structure']:
                            for message in data['structure']['messages']:
                                if 'title' in message and 'timestamp_ms' in message:
                                    # Convert the timestamp to a date
                                    date = datetime.fromtimestamp(int(message['timestamp_ms']) / 1000).strftime('%Y-%m-%d')
                                    changes.append(["title", message['title'], date])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)