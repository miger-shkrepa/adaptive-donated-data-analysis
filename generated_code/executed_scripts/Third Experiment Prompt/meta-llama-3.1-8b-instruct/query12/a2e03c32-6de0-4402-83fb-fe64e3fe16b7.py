import csv
import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])

# Initialize the week and messages sent counters
week = None
messages_sent = 0

# Iterate over the subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is a conversation directory
    if "inbox" in dirnames:
        dirnames.remove("inbox")
        conversation_dir = os.path.join(dirpath, "inbox")
        # Iterate over the message files in the conversation directory
        for filename in os.listdir(conversation_dir):
            if filename.startswith("message_") and filename.endswith(".json"):
                message_file = os.path.join(conversation_dir, filename)
                try:
                    with open(message_file, "r") as file:
                        message_data = json.load(file)
                        # Extract the timestamp from the message data
                        timestamp = message_data["timestamp"]
                        # Convert the timestamp to a datetime object
                        dt = datetime.fromtimestamp(timestamp)
                        # Get the week number from the datetime object
                        week_num = dt.strftime("%Y-%W")
                        # If the week number is different from the previous one, write the previous week to the output file and reset the week and messages sent counters
                        if week_num != week:
                            if week is not None:
                                writer.writerow([week, messages_sent])
                            week = week_num
                            messages_sent = 0
                        # Increment the messages sent counter
                        messages_sent += 1
                except FileNotFoundError:
                    # If the message file does not exist, treat its contribution as 0
                    pass
                except json.JSONDecodeError:
                    # If the message file is not a valid JSON file, treat its contribution as 0
                    pass

# Write the last week to the output file
if week is not None:
    writer.writerow([week, messages_sent])