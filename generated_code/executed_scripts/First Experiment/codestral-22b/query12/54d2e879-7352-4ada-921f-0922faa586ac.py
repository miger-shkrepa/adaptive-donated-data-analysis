import os
import json
import csv
from datetime import datetime

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the messages sent per week
messages_per_week = {}

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    if 'inbox' in foldername:
        for filename in filenames:
            if filename.startswith('message_') and filename.endswith('.json'):
                filepath = os.path.join(foldername, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    for message in data['messages']:
                        timestamp_ms = message.get('timestamp_ms')
                        if timestamp_ms:
                            date = datetime.fromtimestamp(timestamp_ms / 1000)
                            week = date.strftime('%Y-%W')
                            if week in messages_per_week:
                                messages_per_week[week] += 1
                            else:
                                messages_per_week[week] = 1

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])
    for week, count in messages_per_week.items():
        writer.writerow([f'Week {week}', count])