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
        # Iterate over each file in the subdirectory
        for subfilename in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if subfilename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename, subfilename), 'r') as file:
                    # Read the JSON file
                    data = file.read()
                    # Parse the JSON data
                    import json
                    parsed_data = json.loads(data)
                    # Check if the JSON data contains the required information
                    if 'messages' in parsed_data and 'inbox' in parsed_data['messages'] and 'message_1.json' in parsed_data['messages']['inbox']:
                        # Initialize the week and messages sent
                        week = None
                        messages_sent = 0
                        # Iterate over each message in the JSON data
                        for message in parsed_data['messages']['inbox']['message_1.json']['messages']:
                            # Check if the message contains the required information
                            if 'timestamp_ms' in message and 'sender_name' in message:
                                # Extract the week from the timestamp
                                timestamp = int(message['timestamp_ms']) // (1000 * 60 * 60 * 24 * 7)
                                # Check if the week is different from the previous week
                                if week is None or timestamp // (1000 * 60 * 60 * 24 * 7) != week:
                                    # Update the week and reset the messages sent
                                    week = timestamp // (1000 * 60 * 60 * 24 * 7)
                                    messages_sent = 0
                                # Increment the messages sent
                                messages_sent += 1
                        # Append the result to the list
                        results.append([f"Week {week}-01", messages_sent])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['Week', 'Messages Sent'])
    # Write the results
    writer.writerows(results)

print("The results have been written to query_responses/results.csv.")