import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        if not os.path.exists(inbox_dir):
            raise FileNotFoundError("FileNotFoundError: The inbox directory does not exist.")

        messages_sent_per_week = {}

        for conversation_dir in os.listdir(inbox_dir):
            conversation_dir_path = os.path.join(inbox_dir, conversation_dir)
            if not os.path.isdir(conversation_dir_path):
                continue

            for filename in os.listdir(conversation_dir_path):
                if not filename.startswith("message_") or not filename.endswith(".json"):
                    continue

                file_path = os.path.join(conversation_dir_path, filename)
                with open(file_path, "r") as file:
                    data = json.load(file)
                    for message in data["messages"]:
                        timestamp_ms = message["timestamp_ms"]
                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                        week = timestamp.strftime("%Y-%W")
                        if week not in messages_sent_per_week:
                            messages_sent_per_week[week] = 0
                        messages_sent_per_week[week] += 1

        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, messages_sent in messages_sent_per_week.items():
                writer.writerow([f"Week {week}", messages_sent])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_messages_sent_per_week(root_dir)