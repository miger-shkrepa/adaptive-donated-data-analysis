import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    messages_sent_per_week = {}

    # Check if root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Iterate over subfolders in inbox directory
    inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
    if not os.path.exists(inbox_dir):
        return messages_sent_per_week

    for subfolder in os.listdir(inbox_dir):
        subfolder_path = os.path.join(inbox_dir, subfolder)

        # Check if subfolder is a directory
        if not os.path.isdir(subfolder_path):
            continue

        # Iterate over message_X.json files in subfolder
        for filename in os.listdir(subfolder_path):
            if not filename.startswith("message_") or not filename.endswith(".json"):
                continue

            file_path = os.path.join(subfolder_path, filename)

            # Check if file exists
            if not os.path.exists(file_path):
                continue

            # Read JSON file
            with open(file_path, "r") as file:
                data = json.load(file)

            # Iterate over messages
            for message in data["messages"]:
                # Check if message is sent by user
                if message["sender_name"] != "str":  # Replace with actual user name
                    continue

                # Get timestamp
                timestamp_ms = message["timestamp_ms"]
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000)

                # Get week
                week = timestamp.strftime("%Y-%W")

                # Increment messages sent for week
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
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Week", "Messages Sent"])