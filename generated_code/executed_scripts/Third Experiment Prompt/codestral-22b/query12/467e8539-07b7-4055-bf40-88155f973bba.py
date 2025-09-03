import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

messages_sent_per_week = {}

for user_folder in os.listdir(os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")):
    user_folder_path = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox", user_folder)
    if os.path.isdir(user_folder_path):
        for message_file in sorted(os.listdir(user_folder_path)):
            if message_file.startswith("message_") and message_file.endswith(".json"):
                try:
                    with open(os.path.join(user_folder_path, message_file), "r") as f:
                        data = json.load(f)
                        for message in data["messages"]:
                            timestamp = message["timestamp_ms"] / 1000  # Convert to seconds
                            date = datetime.fromtimestamp(timestamp)
                            week = date.strftime('%Y-%W')
                            if week in messages_sent_per_week:
                                messages_sent_per_week[week] += 1
                            else:
                                messages_sent_per_week[week] = 1
                except FileNotFoundError:
                    print(f"FileNotFoundError: The file {message_file} does not exist.")
                except json.JSONDecodeError:
                    print(f"JSONDecodeError: The file {message_file} is not a valid JSON file.")

# Write the results to a CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in messages_sent_per_week.items():
        writer.writerow([week, count])