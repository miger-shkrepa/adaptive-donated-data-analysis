import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the number of ads viewed per company
ads_viewed = {}

# Define the path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_path):
    # Load the JSON data from the posts_viewed.json file
    with open(posts_viewed_path, "r") as f:
        data = json.load(f)

    # Iterate over the impressions_history_posts_seen list
    for post in data["impressions_history_posts_seen"]:
        # Get the author of the post
        author = post["string_map_data"]["Author"]["value"]

        # Increment the number of ads viewed for the author
        if author in ads_viewed:
            ads_viewed[author] += 1
        else:
            ads_viewed[author] = 1

# Define the path to the videos_watched.json file
videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

# Check if the videos_watched.json file exists
if os.path.exists(videos_watched_path):
    # Load the JSON data from the videos_watched.json file
    with open(videos_watched_path, "r") as f:
        data = json.load(f)

    # Iterate over the impressions_history_videos_watched list
    for video in data["impressions_history_videos_watched"]:
        # Get the author of the video
        author = video["string_map_data"]["Author"]["value"]

        # Increment the number of ads viewed for the author
        if author in ads_viewed:
            ads_viewed[author] += 1
        else:
            ads_viewed[author] = 1

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for author, count in ads_viewed.items():
        writer.writerow([author, count])