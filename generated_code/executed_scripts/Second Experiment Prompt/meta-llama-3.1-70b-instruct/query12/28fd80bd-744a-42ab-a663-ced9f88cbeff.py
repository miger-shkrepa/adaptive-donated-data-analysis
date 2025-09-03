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
                with open(os.path.join(dirpath, filename), "r") as file:
                    data = json.load(file)
                    for message in data["messages"]:
                        timestamp_ms = message["timestamp_ms"]
                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                        week = timestamp.strftime("%Y-%W")
                        if week not in messages_sent_per_week:
                            messages_sent_per_week[week] = 0
                        messages_sent_per_week[week] += 1
    return messages_sent_per_week

def save_to_csv(messages_sent_per_week):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Week", "Messages Sent"])
        for week, messages_sent in messages_sent_per_week.items():
            writer.writerow([f"Week {week}", messages_sent])

try:
    messages_sent_per_week = get_messages_sent_per_week(root_dir)
    save_to_csv(messages_sent_per_week)
except FileNotFoundError:
    raise FileNotFoundError("Error: The root directory does not exist.")
except Exception as e:
    raise Exception(f"Error: {str(e)}")