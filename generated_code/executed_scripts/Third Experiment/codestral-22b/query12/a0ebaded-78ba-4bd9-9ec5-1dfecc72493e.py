import os
import json
import csv
from datetime import datetime, timedelta

# Declare the root directory
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
                        if 'sender_name' in message and message['sender_name'] == 'user':
                            timestamp = int(message['timestamp_ms'])
                            date = datetime.fromtimestamp(timestamp / 1000)
                            week = date.strftime('%Y-%W')
                            if week in messages_per_week:
                                messages_per_week[week] += 1
                            else:
                                messages_per_week[week] = 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Week', 'Messages Sent'])
    for week, count in messages_per_week.items():
        writer.writerow(['Week ' + week, count])