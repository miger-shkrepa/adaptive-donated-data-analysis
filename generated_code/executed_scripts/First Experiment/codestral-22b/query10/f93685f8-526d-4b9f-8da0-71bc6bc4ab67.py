import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the results
results = {}

# Define the JSON files to be analyzed
json_files = ["posts_viewed.json", "videos_watched.json"]

# Loop through the JSON files
for file in json_files:
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", file)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file} does not exist.")

    # Open the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the relevant data
    if file == "posts_viewed.json":
        content_data = data["impressions_history_posts_seen"]
    else:
        content_data = data["impressions_history_videos_watched"]

    # Loop through the data and update the results dictionary
    for item in content_data:
        author = item["string_map_data"]["Author"]["value"]
        if author not in results:
            results[author] = {"Post Views": 0, "Video Views": 0}
        if file == "posts_viewed.json":
            results[author]["Post Views"] += 1
        else:
            results[author]["Video Views"] += 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, views in results.items():
        writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})