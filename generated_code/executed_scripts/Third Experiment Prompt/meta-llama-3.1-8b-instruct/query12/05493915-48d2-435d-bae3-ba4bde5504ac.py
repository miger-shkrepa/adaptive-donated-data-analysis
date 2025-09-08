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
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])

    # Iterate over all subdirectories in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the subdirectory is an inbox directory
        if dirnames and dirnames[0] == "inbox":
            # Get the week number from the directory path
            week_dir = os.path.basename(dirpath)
            try:
                week = datetime.strptime(week_dir, "%Y-%m-%d").strftime("%Y-%W")
            except ValueError:
                # If the directory path does not match the expected format, treat its contribution as 0
                week = "Unknown"
                total_messages = 0
            else:
                # Initialize the total messages sent for the week
                total_messages = 0

                # Iterate over all message files in the inbox directory
                for filename in filenames:
                    if filename.startswith("message_") and filename.endswith(".json"):
                        # Get the file path
                        filepath = os.path.join(dirpath, filename)

                        # Check if the file exists
                        if os.path.exists(filepath):
                            try:
                                # Open the file and load the JSON data
                                with open(filepath, 'r') as file:
                                    data = json.load(file)

                                # Get the messages from the JSON data
                                messages = data.get("messages", [])

                                # Increment the total messages sent for the week
                                total_messages += len(messages)
                            except json.JSONDecodeError:
                                # If the file is not a valid JSON file, treat its contribution as 0
                                pass

            # Write the week and total messages sent to the output CSV file
            writer.writerow([week, total_messages])