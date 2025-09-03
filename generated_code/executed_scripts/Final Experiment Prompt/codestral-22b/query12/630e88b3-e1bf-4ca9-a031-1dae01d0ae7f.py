import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

messages_per_week = {}

for subdir, dirs, files in os.walk(os.path.join(root_dir, "your_instagram_activity/messages/inbox")):
    for file in sorted(files):
        if file.startswith("message_") and file.endswith(".json"):
            try:
                with open(os.path.join(subdir, file)) as f:
                    data = json.load(f)
                    for message in data["messages"]:
                        if "sender_name" in message and "timestamp_ms" in message:
                            timestamp = int(message["timestamp_ms"]) / 1000.0
                            week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
                            if week in messages_per_week:
                                messages_per_week[week] += 1
                            else:
                                messages_per_week[week] = 1
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing file {file}: {e}")

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in messages_per_week.items():
        writer.writerow([f"Week {week}", count])