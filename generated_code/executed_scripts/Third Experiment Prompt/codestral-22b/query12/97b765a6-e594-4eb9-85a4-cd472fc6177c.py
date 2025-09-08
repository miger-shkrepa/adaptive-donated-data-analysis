import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the number of messages sent per week
messages_sent_per_week = {}

# Traverse the directory
for user_folder in os.listdir(os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")):
    user_folder_path = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox", user_folder)

    # Check if the user folder is a directory
    if os.path.isdir(user_folder_path):
        for message_file in sorted(os.listdir(user_folder_path)):
            if message_file.startswith("message_") and message_file.endswith(".json"):
                message_file_path = os.path.join(user_folder_path, message_file)

                # Try to open and read the message file
                try:
                    with open(message_file_path, "r") as f:
                        data = json.load(f)

                    # Check if the data is a dictionary and contains the 'messages' key
                    if isinstance(data, dict) and 'messages' in data:
                        for message in data['messages']:
                            # Check if the message contains the 'timestamp_ms' key
                            if 'timestamp_ms' in message:
                                # Convert the timestamp to a datetime object
                                timestamp = datetime.fromtimestamp(message['timestamp_ms'] / 1000)

                                # Get the week number
                                week = timestamp.strftime('%Y-%W')

                                # Increment the number of messages sent for this week
                                if week in messages_sent_per_week:
                                    messages_sent_per_week[week] += 1
                                else:
                                    messages_sent_per_week[week] = 1
                except Exception as e:
                    print(f"Error reading file {message_file_path}: {e}")

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in messages_sent_per_week.items():
        writer.writerow([f"Week {week}", count])