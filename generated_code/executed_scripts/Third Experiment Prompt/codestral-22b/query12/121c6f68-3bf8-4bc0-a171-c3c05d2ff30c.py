import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

messages_sent_per_week = {}

inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")

for conversation_dir in os.listdir(inbox_dir):
    conversation_path = os.path.join(inbox_dir, conversation_dir)

    if os.path.isdir(conversation_path):
        for message_file in sorted(os.listdir(conversation_path)):
            if message_file.startswith("message_") and message_file.endswith(".json"):
                message_path = os.path.join(conversation_path, message_file)

                with open(message_path, "r") as f:
                    try:
                        data = json.load(f)
                        for message in data["messages"]:
                            timestamp = message["timestamp_ms"] / 1000.0
                            date = datetime.fromtimestamp(timestamp)
                            week = date.strftime('%Y-%W')

                            if week not in messages_sent_per_week:
                                messages_sent_per_week[week] = 0

                            messages_sent_per_week[week] += 1
                    except json.JSONDecodeError:
                        print(f"Warning: Could not decode JSON in file {message_path}")

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Week", "Messages Sent"])

    for week, count in messages_sent_per_week.items():
        writer.writerow([f"Week {week}", count])