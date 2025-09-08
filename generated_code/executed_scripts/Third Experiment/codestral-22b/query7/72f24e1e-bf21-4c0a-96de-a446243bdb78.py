import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store user engagement with stories
user_engagement = {}

# Traverse the directory structure
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.json') and 'stories' in root:
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    if 'messages' in data:
                        for message in data['messages']:
                            if 'sender_name' in message:
                                user = message['sender_name']
                                if user in user_engagement:
                                    user_engagement[user] += 1
                                else:
                                    user_engagement[user] = 1
            except Exception as e:
                print(f"Error processing file {file}: {str(e)}")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Times Engaged'])
    for user, times in user_engagement.items():
        writer.writerow([user, times])