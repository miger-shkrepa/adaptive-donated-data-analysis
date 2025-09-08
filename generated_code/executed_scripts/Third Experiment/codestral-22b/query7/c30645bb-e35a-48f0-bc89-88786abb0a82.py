import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store user engagement
user_engagement = {}

# Traverse through the directory structure
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'structure' in data and 'messages' in data['structure']:
                        for message in data['structure']['messages']:
                            if 'sender_name' in message:
                                sender_name = message['sender_name']
                                if sender_name in user_engagement:
                                    user_engagement[sender_name] += 1
                                else:
                                    user_engagement[sender_name] = 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Times Engaged'])
    for user, times in user_engagement.items():
        writer.writerow([user, times])