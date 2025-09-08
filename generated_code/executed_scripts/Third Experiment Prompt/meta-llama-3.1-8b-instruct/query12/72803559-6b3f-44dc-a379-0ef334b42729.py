import os
import csv
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])

    # Iterate over all subdirectories in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the subdirectory is the 'inbox' directory
        if "inbox" in dirnames:
            # Iterate over all message_X.json files in the subdirectory
            for filename in filenames:
                if filename.startswith("message_") and filename.endswith(".json"):
                    # Open the JSON file
                    with open(os.path.join(dirpath, filename), "r") as jsonfile:
                        data = json.load(jsonfile)

                        # Extract the week from the file path
                        week = datetime.fromtimestamp(os.path.getctime(os.path.join(dirpath, filename))).strftime("%Y-%W")

                        # Initialize the messages sent count
                        messages_sent = 0

                        # Iterate over all messages in the JSON file
                        for message in data["messages"]:
                            # Increment the messages sent count
                            messages_sent += 1

                        # Write the week and messages sent to the output CSV file
                        with open(output_file, "a", newline="") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([week, messages_sent])