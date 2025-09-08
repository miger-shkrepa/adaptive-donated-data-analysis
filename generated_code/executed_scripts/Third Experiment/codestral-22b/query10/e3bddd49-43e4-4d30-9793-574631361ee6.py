import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the data
data = {}

# Define the paths to the JSON files
posts_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
videos_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

# Process the posts file
if os.path.exists(posts_file):
    with open(posts_file, "r") as f:
        posts_data = json.load(f)
    for post in posts_data["impressions_history_posts_seen"]:
        author = post["string_map_data"]["Author"]["value"]
        if author not in data:
            data[author] = {"Post Views": 0, "Video Views": 0}
        data[author]["Post Views"] += 1

# Process the videos file
if os.path.exists(videos_file):
    with open(videos_file, "r") as f:
        videos_data = json.load(f)
    for video in videos_data["impressions_history_videos_watched"]:
        author = video["string_map_data"]["Author"]["value"]
        if author not in data:
            data[author] = {"Post Views": 0, "Video Views": 0}
        data[author]["Video Views"] += 1

# Write the data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account", "Post Views", "Video Views"])
    for author, views in data.items():
        writer.writerow([author, views["Post Views"], views["Video Views"]])