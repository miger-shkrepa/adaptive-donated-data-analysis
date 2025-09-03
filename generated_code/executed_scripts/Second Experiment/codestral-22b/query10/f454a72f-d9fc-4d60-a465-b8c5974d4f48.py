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

# Define the JSON files to be processed
json_files = ["posts_viewed.json", "videos_watched.json"]

# Iterate over the JSON files
for file in json_files:
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", file)

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Extract the relevant data
        if file == "posts_viewed.json":
            impressions = data.get("impressions_history_posts_seen", [])
        else:
            impressions = data.get("impressions_history_videos_watched", [])

        # Iterate over the impressions
        for impression in impressions:
            author = impression["string_map_data"]["Author"]["value"]

            # Update the results dictionary
            if author in results:
                results[author][file == "posts_viewed.json"] += 1
            else:
                results[author] = [0, 0]
                results[author][file == "posts_viewed.json"] += 1
    else:
        print(f"Warning: {file_path} does not exist.")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    for account, views in results.items():
        writer.writerow([account, views[0], views[1]])