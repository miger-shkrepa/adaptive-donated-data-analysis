import os
import json
import csv
from datetime import datetime, timedelta

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

            # Iterate over all messages in the data
            for message in data["structure"]["messages"]:
                # Check if the message has a timestamp
                if "timestamp_ms" in message:
                    # Convert the timestamp to a datetime object
                    timestamp = datetime.fromtimestamp(int(message["timestamp_ms"]) / 1000)

                    # Get the week number of the timestamp
                    week = timestamp.strftime("%Y-%W")

                    # Increment the messages sent for the week
                    if week in messages_per_week:
                        messages_per_week[week] += 1
                    else:
                        messages_per_week[week] = 1

            # Increment the message file index
            i += 1

# Create the output CSV file
output_file = "query_responses/results.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Week", "Messages Sent"])

    # Write the messages sent per week
    for week, count in messages_per_week.items():
        writer.writerow([f"Week {week}", count])