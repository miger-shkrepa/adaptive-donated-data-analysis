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

# Traverse the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'messages' in dirpath:
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if 'structure' in data and 'title' in data['structure']:
                        title = data['structure']['title']
                        timestamp = data['structure'].get('timestamp', 'Unknown')
                        changes.append((filename, title, timestamp))

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    for change in changes:
        filename, new_value, timestamp = change
        try:
            change_date = datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d')
        except ValueError:
            change_date = 'Unknown'
        writer.writerow([filename, new_value, change_date])