import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_per_week(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the messages per week
        messages_per_week = {}

        # Iterate over the inbox directory
        inbox_dir = os.path.join(root_dir, "inbox")
        if os.path.exists(inbox_dir):
            for conversation_dir in os.listdir(inbox_dir):
                conversation_path = os.path.join(inbox_dir, conversation_dir)
                if os.path.isdir(conversation_path):
                    for filename in os.listdir(conversation_path):
                        if filename.startswith("message_") and filename.endswith(".json"):
                            message_path = os.path.join(conversation_path, filename)
                            with open(message_path, "r") as file:
                                message_data = json.load(file)
                                for message in message_data:
                                    if "timestamp_ms" in message:
                                        timestamp = int(message["timestamp_ms"])
                                        date = datetime.fromtimestamp(timestamp / 1000)
                                        week = date.strftime("Week %Y-%U")
                                        if week not in messages_per_week:
                                            messages_per_week[week] = 0
                                        if "sender_name" in message:
                                            messages_per_week[week] += 1

        # Write the results to a CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Week", "Messages Sent"])
            for week, messages in messages_per_week.items():
                writer.writerow([week, messages])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON: {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")

get_messages_per_week(root_dir)