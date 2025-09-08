import os
import json
import csv
from datetime import datetime

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the messages sent per week
messages_per_week = {}

# Traverse the directory structure
for folder_name in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder_name)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.startswith("message_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r") as file:
                    data = json.load(file)
                    messages = data["structure"]["messages"]
                    for message in messages:
                        timestamp_ms = message["timestamp_ms"]
                        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                        week = timestamp.strftime("%Y-%W")
                        if week in messages_per_week:
                            messages_per_week[week] += 1
                        else:
                            messages_per_week[week] = 1

# Create the output CSV file
output_file = "query_responses/results.csv"
with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Week", "Messages Sent"])
    for week, count in messages_per_week.items():
        writer.writerow([f"Week {week}", count])

print("The CSV file has been generated successfully.")