import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    messages_sent_per_week = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")):
        for filename in filenames:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data["messages"]:
                            timestamp_ms = message["timestamp_ms"]
                            timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                            week = timestamp.strftime("%Y-%W")
                            if week not in messages_sent_per_week:
                                messages_sent_per_week[week] = 0
                            messages_sent_per_week[week] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file {} does not exist.".format(file_path))
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))
                except KeyError:
                    raise ValueError("Error: The file {} is missing required keys.".format(file_path))
    return messages_sent_per_week

def save_to_csv(messages_sent_per_week):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Week", "Messages Sent"])
        for week, messages_sent in messages_sent_per_week.items():
            writer.writerow([week, messages_sent])

try:
    messages_sent_per_week = get_messages_sent_per_week(root_dir)
    save_to_csv(messages_sent_per_week)
except FileNotFoundError:
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Week", "Messages Sent"])