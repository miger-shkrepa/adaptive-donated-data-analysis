import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

messages_per_week = {}

inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")

for user_dir in os.listdir(inbox_dir):
    user_path = os.path.join(inbox_dir, user_dir)
    if os.path.isdir(user_path):
        for message_file in sorted(os.listdir(user_path)):
            if message_file.startswith("message_") and message_file.endswith(".json"):
                with open(os.path.join(user_path, message_file), "r") as f:
                    try:
                        data = json.load(f)
                        for message in data["messages"]:
                            timestamp = message["timestamp_ms"]
                            date = datetime.fromtimestamp(timestamp / 1000)
                            week = date.strftime('%Y-%W')
                            if week in messages_per_week:
                                messages_per_week[week] += 1
                            else:
                                messages_per_week[week] = 1
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode JSON in file {message_file}")

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in messages_per_week.items():
        writer.writerow([f"Week {week}", count])