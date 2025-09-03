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
        # Check if the subdirectory is an 'inbox' directory
        if "inbox" in dirnames:
            dirnames.remove("inbox")
            inbox_dir = os.path.join(dirpath, "inbox")

            # Initialize the total messages sent for the week
            total_messages_sent = 0

            # Iterate over all message files in the inbox directory
            for filename in os.listdir(inbox_dir):
                if filename.startswith("message_") and filename.endswith(".json"):
                    message_file = os.path.join(inbox_dir, filename)

                    # Try to open and parse the message file
                    try:
                        with open(message_file, "r") as file:
                            message_data = json.load(file)

                            # Extract the timestamp from the message data
                            timestamp = message_data["timestamp_ms"]

                            # Convert the timestamp to a datetime object
                            date = datetime.fromtimestamp(timestamp / 1000)

                            # Get the week number from the datetime object
                            week_number = date.strftime("%Y-%W")

                            # Increment the total messages sent for the week
                            total_messages_sent += 1

                            # Write the week and total messages sent to the output CSV file
                            with open(output_file, "a", newline="") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([week_number, total_messages_sent])

                    # Handle any errors that occur while opening or parsing the message file
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        print(f"Error: {e}")

# Print a success message
print("Query completed successfully.")