import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Initialize dictionary to store messages sent per week
        messages_sent_per_week = {}

        # Iterate over inbox directories
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                # Iterate over message files in conversation directory
                for message_file in os.listdir(conversation_path):
                    if message_file.startswith("message_") and message_file.endswith(".json"):
                        message_path = os.path.join(conversation_path, message_file)
                        with open(message_path, "r") as f:
                            message_data = json.load(f)
                            # Get timestamp of message
                            timestamp = message_data["messages"][0]["timestamp_ms"]
                            # Convert timestamp to datetime object
                            dt = datetime.fromtimestamp(timestamp / 1000)
                            # Get week of the year
                            week = dt.strftime("%Y-%W")
                            # Increment messages sent for week
                            if week in messages_sent_per_week:
                                messages_sent_per_week[week] += 1
                            else:
                                messages_sent_per_week[week] = 1

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, messages_sent in messages_sent_per_week.items():
                writer.writerow([week, messages_sent])

    except FileNotFoundError as e:
        # Write column headers to CSV file if root directory does not exist
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
        raise e

get_messages_sent_per_week(root_dir)