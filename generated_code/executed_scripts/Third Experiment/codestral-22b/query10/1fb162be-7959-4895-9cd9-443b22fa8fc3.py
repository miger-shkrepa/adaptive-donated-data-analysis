import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the data
data = {}

# Define the JSON files to be processed
json_files = ["posts_viewed.json", "videos_watched.json"]

# Process each JSON file
for file in json_files:
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", file)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning: The file {file} does not exist. Skipping this file.")
        continue

    # Load the JSON data
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    # Extract the relevant data
    if file == "posts_viewed.json":
        data_key = "impressions_history_posts_seen"
    elif file == "videos_watched.json":
        data_key = "impressions_history_videos_watched"

    for item in json_data[data_key]:
        author = item["string_map_data"]["Author"]["value"]
        if author not in data:
            data[author] = {"Post Views": 0, "Video Views": 0}
        if file == "posts_viewed.json":
            data[author]["Post Views"] += 1
        elif file == "videos_watched.json":
            data[author]["Video Views"] += 1

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, views in data.items():
        writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})