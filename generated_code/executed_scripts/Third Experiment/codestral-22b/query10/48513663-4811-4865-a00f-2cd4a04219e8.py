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

# Define the path to the posts_viewed.json file
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    # Open the posts_viewed.json file
    with open(posts_viewed_file, "r") as f:
        # Load the JSON data
        posts_viewed_data = json.load(f)

        # Iterate over the posts_viewed_data
        for post in posts_viewed_data["impressions_history_posts_seen"]:
            # Get the author of the post
            author = post["string_map_data"]["Author"]["value"]

            # If the author is not in the data dictionary, add it
            if author not in data:
                data[author] = {"Post Views": 1, "Video Views": 0}
            else:
                # Increment the post views for the author
                data[author]["Post Views"] += 1

# Define the path to the video views directory
video_views_dir = os.path.join(root_dir, "202312", "202401", "202402")

# Iterate over the video views directory
for dirpath, dirnames, filenames in os.walk(video_views_dir):
    for filename in filenames:
        # Check if the file is a video file
        if filename.endswith(".mp4"):
            # Get the author of the video
            author = filename.split("_")[0]

            # If the author is not in the data dictionary, add it
            if author not in data:
                data[author] = {"Post Views": 0, "Video Views": 1}
            else:
                # Increment the video views for the author
                data[author]["Video Views"] += 1

# Write the data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Write the data rows
    for account, views in data.items():
        writer.writerow([account, views["Post Views"], views["Video Views"]])