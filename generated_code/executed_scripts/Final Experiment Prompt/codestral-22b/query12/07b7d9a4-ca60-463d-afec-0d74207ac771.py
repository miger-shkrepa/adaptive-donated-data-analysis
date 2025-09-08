import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

messages_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
if not os.path.exists(messages_dir):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Week", "Messages Sent"])
    raise FileNotFoundError("Error: The messages directory does not exist.")

weekly_messages = {}

for subdir in os.listdir(messages_dir):
    subdir_path = os.path.join(messages_dir, subdir)
    if os.path.isdir(subdir_path):
        for filename in sorted(os.listdir(subdir_path)):
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(subdir_path, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for message in data["messages"]:
                            if "timestamp_ms" in message:
                                try:
                                    timestamp = int(message["timestamp_ms"])
                                    week = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%W')
                                    if week in weekly_messages:
                                        weekly_messages[week] += 1
                                    else:
                                        weekly_messages[week] = 1
                                except ValueError:
                                    print(f"Error: Invalid timestamp value in {file_path}")
                except FileNotFoundError:
                    print(f"Error: The file {file_path} does not exist.")

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in sorted(weekly_messages.items()):
        writer.writerow([f"Week {week}", count])