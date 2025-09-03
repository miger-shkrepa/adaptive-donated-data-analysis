import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over each subfolder in the inbox directory
for folder in os.listdir(root_dir):
    # Check if the subfolder is a directory
    if os.path.isdir(os.path.join(root_dir, folder)):
        # Initialize the week and messages sent for the current folder
        week = None
        messages_sent = 0

        # Iterate over each message file in the subfolder
        for file in os.listdir(os.path.join(root_dir, folder)):
            # Check if the file is a message file
            if file.startswith("message_") and file.endswith(".json"):
                # Extract the week from the file name
                week_str = file.split("_")[1].split(".")[0]
                if week is None or week != week_str:
                    # If this is the first message file for the week, update the week and reset the messages sent
                    week = week_str
                    messages_sent = 0

                # Try to read the message file
                try:
                    with open(os.path.join(root_dir, folder, file), "r") as f:
                        # Read the message file
                        data = f.read()

                        # Parse the message data
                        import json
                        message_data = json.loads(data)

                        # Check if the message data contains a timestamp
                        if "timestamp_ms" in message_data:
                            # Increment the messages sent for the current week
                            messages_sent += 1
                except Exception as e:
                    # If there is an error reading the message file, print the error and continue
                    print(f"Error reading message file {file}: {e}")

        # Append the results for the current folder to the list
        results.append((week, messages_sent))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Week", "Messages Sent"])  # Write the column headers
    for result in results:
        writer.writerow(result)