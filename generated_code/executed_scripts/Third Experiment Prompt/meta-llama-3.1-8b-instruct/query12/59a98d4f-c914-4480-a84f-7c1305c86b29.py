import os
import csv
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over all subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is an 'inbox' directory
    if 'inbox' in dirnames:
        # Get the subdirectory name (e.g., username_placeholder)
        subdirectory_name = dirpath.split(os.sep)[-1]
        
        # Initialize the week and messages sent for this subdirectory
        week = None
        messages_sent = 0
        
        # Iterate over all files in the subdirectory
        for filename in filenames:
            # Check if the file is a message_X.json file
            if filename.startswith('message_') and filename.endswith('.json'):
                # Extract the week from the file name (e.g., message_1.json -> Week 2025-02)
                file_week = datetime.datetime.strptime(filename.split('_')[1].split('.')[0], '%Y-%m-%d').strftime('%Y-%W')
                
                # If this is the first file in the subdirectory, set the week
                if week is None:
                    week = file_week
                
                # Read the JSON file
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        
                        # Iterate over all messages in the file
                        for message in data['messages']:
                            # Increment the messages sent count
                            messages_sent += 1
                except json.JSONDecodeError:
                    # If the file is not a valid JSON file, treat its contribution as 0
                    pass
        
        # Append the results for this subdirectory to the results list
        results.append((week, messages_sent))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Week', 'Messages Sent'])
    writer.writerows(results)