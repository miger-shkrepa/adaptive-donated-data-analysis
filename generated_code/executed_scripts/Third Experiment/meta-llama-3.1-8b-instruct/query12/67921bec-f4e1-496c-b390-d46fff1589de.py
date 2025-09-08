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
        # Initialize the week and messages sent for the current directory
        week = None
        messages_sent = 0

        # Iterate over each file in the directory
        for file in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, file), 'r') as f:
                    # Load the JSON data
                    data = json.load(f)

                    # Check if the JSON data contains the required information
                    if 'messages' in data and 'inbox' in data['messages']:
                        # Iterate over each message in the inbox
                        for message in data['messages']['inbox'].values():
                            # Check if the message is a JSON file
                            if 'message_1.json' in message:
                                # Open the JSON file
                                with open(os.path.join(root_dir, filename, message['message_1.json']), 'r') as f:
                                    # Load the JSON data
                                    message_data = json.load(f)

                                    # Check if the JSON data contains the required information
                                    if 'messages' in message_data and 'content' in message_data['messages'][0]:
                                        # Extract the week from the filename
                                        week = filename.split('_')[0]

                                        # Increment the messages sent
                                        messages_sent += 1

        # Append the results to the list
        results.append([week, messages_sent])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])  # header
    writer.writerows(results)