import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the messages sent per week
messages_per_week = {}

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a directory
    if os.path.isdir(os.path.join(root_dir, filename)):
        # Initialize a counter for messages sent in the current week
        messages_sent = 0
        
        # Iterate over each file in the current directory
        for file in os.listdir(os.path.join(root_dir, filename)):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file and read its contents
                with open(os.path.join(root_dir, filename, file), 'r') as f:
                    data = f.read()
                    
                    # Parse the JSON data
                    import json
                    parsed_data = json.loads(data)
                    
                    # Check if the JSON data contains a 'messages' key
                    if 'messages' in parsed_data:
                        # Iterate over each message in the JSON data
                        for message in parsed_data['messages']:
                            # Check if the message has a 'timestamp_ms' key
                            if 'timestamp_ms' in message:
                                # Calculate the week from the timestamp
                                import datetime
                                timestamp = int(message['timestamp_ms'])
                                date = datetime.datetime.fromtimestamp(timestamp / 1000)
                                week = date.strftime('%Y-%W')
                                
                                # Increment the messages sent counter for the current week
                                messages_sent += 1
                                if week in messages_per_week:
                                    messages_per_week[week] += 1
                                else:
                                    messages_per_week[week] = 1
        
        # Write the messages sent per week to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the column headers
            writer.writeheader()
            
            # Write the messages sent per week
            for week, messages in messages_per_week.items():
                writer.writerow({'Week': week, 'Messages Sent': messages})

# If the necessary files or directories do not exist in the structure, return a CSV file with only the column headers
if not messages_per_week:
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the column headers
        writer.writeheader()