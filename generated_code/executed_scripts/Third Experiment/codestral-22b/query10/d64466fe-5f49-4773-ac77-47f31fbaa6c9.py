import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the data
data = []

# Traverse the directory structure
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if 'structure' in json_data and 'media_list_data' in json_data['structure']:
                        for item in json_data['structure']['media_list_data']:
                            account = item.get('value', '')
                            post_views = item.get('post_views', 0)
                            video_views = item.get('video_views', 0)
                            data.append([account, post_views, video_views])
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    writer.writerows(data)