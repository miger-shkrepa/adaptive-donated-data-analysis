import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the messages per week
messages_per_week = {}

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        # Iterate over each file in the directory
        for file in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, file), 'r') as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the JSON data contains messages
                    if 'messages' in data:
                        # Iterate over each message
                        for message in data['messages']:
                            # Check if the message has a timestamp
                            if 'timestamp_ms' in message:
                                # Get the week from the timestamp
                                week = message['timestamp_ms'] // (7 * 24 * 60 * 60 * 1000)
                                # Increment the messages per week
                                messages_per_week[week] = messages_per_week.get(week, 0) + 1

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])
    # Iterate over each week and its messages
    for week, messages in messages_per_week.items():
        # Write the week and messages to the CSV file
        writer.writerow([f'Week {week}', messages])