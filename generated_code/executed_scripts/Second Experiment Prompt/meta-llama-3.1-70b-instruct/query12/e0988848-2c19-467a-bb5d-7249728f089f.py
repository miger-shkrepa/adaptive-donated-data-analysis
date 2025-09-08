import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    messages_sent = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")):
        for filename in filenames:
            if filename.startswith("message_") and filename.endswith(".json"):
                with open(os.path.join(dirpath, filename), "r") as f:
                    data = json.load(f)
                    for message in data["messages"]:
                        timestamp = message["timestamp_ms"] / 1000
                        date = datetime.fromtimestamp(timestamp)
                        week = date.strftime("%Y-%W")
                        if week not in messages_sent:
                            messages_sent[week] = 0
                        messages_sent[week] += 1
    return messages_sent

def write_to_csv(messages_sent):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Week", "Messages Sent"])
        for week, count in messages_sent.items():
            writer.writerow([f"Week {week}", count])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    messages_sent = get_messages_sent_per_week(root_dir)
    write_to_csv(messages_sent)
except FileNotFoundError as e:
    raise FileNotFoundError(f"FileNotFoundError: {e}")
except Exception as e:
    raise ValueError(f"Error: {e}")