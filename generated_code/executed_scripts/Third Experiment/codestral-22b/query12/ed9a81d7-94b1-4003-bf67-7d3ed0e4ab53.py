import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the messages sent per week
messages_per_week = {}

# Iterate over all subdirectories in the root directory
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)

    # Check if the subdirectory is a directory
    if os.path.isdir(subdir_path):

        # Iterate over all message files in the subdirectory
        i = 1
        while True:
            message_file = os.path.join(subdir_path, f"message_{i}.json")

            # Check if the message file exists
            if not os.path.exists(message_file):
                break

            # Open the message file and load the JSON data
            with open(message_file, "r") as f:
                data = json.load(f)

            # Extract the timestamp from the JSON data
            timestamp_ms = data.get("timestamp_ms")

            # Check if the timestamp is valid
            if timestamp_ms is None:
                raise ValueError("ValueError: Invalid timestamp in message file.")

            # Convert the timestamp to a datetime object
            timestamp = datetime.fromtimestamp(int(timestamp_ms) / 1000)

            # Extract the week number from the timestamp
            week = timestamp.strftime("%Y-%W")

            # Increment the messages sent for the corresponding week
            if week in messages_per_week:
                messages_per_week[week] += 1
            else:
                messages_per_week[week] = 1

            # Increment the message file index
            i += 1

# Create a CSV file with the messages sent per week
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Week", "Messages Sent"])

    # Sort the messages sent per week by week number
    sorted_messages_per_week = sorted(messages_per_week.items(), key=lambda x: x[0])

    # Write the messages sent per week to the CSV file
    for week, messages_sent in sorted_messages_per_week:
        writer.writerow([f"Week {week}", messages_sent])