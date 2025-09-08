import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

messages_sent_per_week = {}

for conversation_dir in os.listdir(root_dir):
    conversation_path = os.path.join(root_dir, conversation_dir)
    if os.path.isdir(conversation_path):
        for message_file in sorted(os.listdir(conversation_path)):
            if message_file.startswith("message_") and message_file.endswith(".json"):
                try:
                    with open(os.path.join(conversation_path, message_file), 'r') as f:
                        message_data = json.load(f)
                        timestamp = message_data.get('timestamp')
                        if timestamp:
                            date = datetime.fromtimestamp(timestamp)
                            week = date.strftime('%Y-%W')
                            messages_sent_per_week[week] = messages_sent_per_week.get(week, 0) + 1
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error processing file {message_file}: {e}")

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in messages_sent_per_week.items():
        writer.writerow([f"Week {week}", count])