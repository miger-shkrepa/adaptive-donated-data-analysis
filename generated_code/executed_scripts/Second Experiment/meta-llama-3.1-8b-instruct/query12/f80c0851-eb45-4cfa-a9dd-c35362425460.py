import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

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
                    # Check if the JSON data has the required structure
                    if 'messages' in data and 'inbox' in data['messages'] and 'username_placeholder' in data['messages']['inbox']:
                        # Initialize the total messages sent
                        total_messages_sent = 0
                        # Initialize the week
                        week = None
                        # Iterate over each message in the inbox
                        for message in data['messages']['inbox']['username_placeholder']['messages']:
                            # Check if the message has the required structure
                            if 'timestamp_ms' in message and 'sender_name' in message:
                                # Get the timestamp
                                timestamp = int(message['timestamp_ms'])
                                # Get the year and week from the timestamp
                                year = timestamp // 604800000
                                week = (timestamp // 604800000) % 52 + 1
                                # Increment the total messages sent
                                total_messages_sent += 1
                        # Append the result to the list
                        results.append((f"Week {year}-W{week}", total_messages_sent))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])
    # Write the results
    for result in results:
        writer.writerow(result)