import os
import json
from datetime import datetime
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the paths to the liked_posts.json and saved_posts.json files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Process the liked_posts.json file
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        liked_posts = json.load(f)
    for post in liked_posts["likes_media_likes"]:
        for data in post["string_list_data"]:
            results.append(["Liked Posts", datetime.fromtimestamp(data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')])

# Process the saved_posts.json file
if os.path.exists(saved_posts_path):
    with open(saved_posts_path, "r") as f:
        saved_posts = json.load(f)
    for post in saved_posts["saved_saved_media"]:
        saved_on = post["string_map_data"]["Saved on"]
        results.append(["Saved Posts", datetime.fromtimestamp(saved_on["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Device ID", "Login Time"])
    writer.writerows(results)