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
        if "inbox" in dirnames:
            # Get the inbox directory path
            inbox_dir = os.path.join(dirpath, "inbox")

            # Initialize the messages sent counter for the current week
            messages_sent = 0

            # Iterate over all files in the inbox directory
            for filename in os.listdir(inbox_dir):
                # Check if the file is a message_X.json file
                if filename.startswith("message_") and filename.endswith(".json"):
                    # Get the file path
                    file_path = os.path.join(inbox_dir, filename)

                    # Try to open and read the file
                    try:
                        with open(file_path, 'r') as file:
                            data = json.load(file)

                            # Get the timestamp of the message
                            timestamp = data["timestamp_ms"]

                            # Convert the timestamp to a datetime object
                            dt = datetime.fromtimestamp(timestamp / 1000)

                            # Get the week of the message
                            week = dt.strftime('%Y-%W')

                            # Increment the messages sent counter for the current week
                            messages_sent += 1

                            # Write the week and messages sent to the output CSV file
                            with open(output_file, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([week, messages_sent])
                    except FileNotFoundError:
                        # If the file does not exist, treat its contribution as 0
                        pass
                    except json.JSONDecodeError:
                        # If the file is not a valid JSON file, treat its contribution as 0
                        pass