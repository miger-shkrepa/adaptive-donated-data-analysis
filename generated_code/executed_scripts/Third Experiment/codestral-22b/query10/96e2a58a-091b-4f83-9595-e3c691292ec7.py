import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the views data
views_data = {}

# Traverse the directory structure
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'structure' in data and 'messages' in data['structure']:
                        for message in data['structure']['messages']:
                            if 'sender_name' in message and 'is_geoblocked_for_viewer' in message and not message['is_geoblocked_for_viewer']:
                                account = message['sender_name']
                                if account not in views_data:
                                    views_data[account] = {'post_views': 0, 'video_views': 0}
                                if 'content' in message:
                                    views_data[account]['post_views'] += 1
                                if 'share' in message and 'link' in message['share']:
                                    if 'instagram.com' in message['share']['link']:
                                        views_data[account]['video_views'] += 1
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for account, views in views_data.items():
        writer.writerow({'Account': account, 'Post Views': views['post_views'], 'Video Views': views['video_views']})