import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the messages sent per week
        messages_sent_per_week = {}

        # Iterate over the inbox directory
        inbox_dir = os.path.join(root_dir, "messages", "inbox")
        if os.path.exists(inbox_dir):
            for conversation_dir in os.listdir(inbox_dir):
                conversation_dir_path = os.path.join(inbox_dir, conversation_dir)
                if os.path.isdir(conversation_dir_path):
                    for filename in os.listdir(conversation_dir_path):
                        if filename.startswith("message_") and filename.endswith(".json"):
                            file_path = os.path.join(conversation_dir_path, filename)
                            with open(file_path, "r") as file:
                                data = json.load(file)
                                for message in data.get("messages", []):
                                    timestamp_ms = message.get("timestamp_ms")
                                    if timestamp_ms:
                                        week = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("Week %Y-%U")
                                        if week not in messages_sent_per_week:
                                            messages_sent_per_week[week] = 0
                                        messages_sent_per_week[week] += 1

        # Write the results to a CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, messages_sent in messages_sent_per_week.items():
                writer.writerow([week, messages_sent])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON file: {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")

    else:
        # If no messages are found, write a CSV file with only the column headers
        if not os.path.exists("query_responses/results.csv") or os.path.getsize("query_responses/results.csv") == 0:
            with open("query_responses/results.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Week", "Messages Sent"])

get_messages_sent_per_week(root_dir)