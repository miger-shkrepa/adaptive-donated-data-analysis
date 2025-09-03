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
for subdir, dirs, files in os.walk(root_dir):
    if 'inbox' in subdir:
        for conversation_dir in dirs:
            conversation_path = os.path.join(subdir, conversation_dir)
            message_files = [f for f in os.listdir(conversation_path) if f.startswith('message_') and f.endswith('.json')]
            message_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))  # Sort the files based on the number

            for message_file in message_files:
                file_path = os.path.join(conversation_path, message_file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        timestamp_ms = data.get('timestamp_ms')
                        if timestamp_ms:
                            date = datetime.fromtimestamp(timestamp_ms / 1000)
                            week = date.strftime('%Y-%W')
                            messages_per_week[week] = messages_per_week.get(week, 0) + 1
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error processing file {file_path}: {str(e)}")

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])
    for week, count in messages_per_week.items():
        writer.writerow([f'Week {week}', count])