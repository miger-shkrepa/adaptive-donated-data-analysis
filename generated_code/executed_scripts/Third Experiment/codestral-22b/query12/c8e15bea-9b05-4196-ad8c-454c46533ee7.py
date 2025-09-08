import os
import json
import csv
from datetime import datetime

# Declare the root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the message count per week
message_count = {}

# Iterate over all subdirectories in the root directory
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)

    # Check if the subdirectory is a directory
    if os.path.isdir(subdir_path):
        # Iterate over all message files in the subdirectory
        for file in os.listdir(subdir_path):
            if file.startswith("message_") and file.endswith(".json"):
                file_path = os.path.join(subdir_path, file)

                # Check if the file exists
                if os.path.exists(file_path):
                    # Open the JSON file and load the data
                    with open(file_path, "r") as f:
                        data = json.load(f)

                    # Extract the timestamp from the data
                    timestamp = data.get("timestamp")

                    # Check if the timestamp is valid
                    if timestamp:
                        # Convert the timestamp to a datetime object
                        dt = datetime.fromtimestamp(timestamp)

                        # Extract the week number and year
                        week = dt.strftime("%Y-%W")

                        # Increment the message count for the corresponding week
                        if week in message_count:
                            message_count[week] += 1
                        else:
                            message_count[week] = 1

# Create the output CSV file
output_file = "query_responses/results.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Week", "Messages Sent"])

    # Write the message count for each week
    for week, count in message_count.items():
        writer.writerow([f"Week {week}", count])

print(f"Results saved to {output_file}")