import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
topics_of_interest = []

# Define the path to the ads_viewed.json file
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Check if the ads_viewed.json file exists
if os.path.exists(ads_viewed_path):
    # Open the ads_viewed.json file
    with open(ads_viewed_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the topics of interest from the data
        for ad in data["impressions_history_ads_seen"]:
            if "string_map_data" in ad and "Topic" in ad["string_map_data"]:
                topics_of_interest.append(ad["string_map_data"]["Topic"]["value"])

# Define the path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_path):
    # Open the posts_viewed.json file
    with open(posts_viewed_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the topics of interest from the data
        for post in data["impressions_history_posts_seen"]:
            if "string_map_data" in post and "Topic" in post["string_map_data"]:
                topics_of_interest.append(post["string_map_data"]["Topic"]["value"])

# Define the path to the videos_watched.json file
videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

# Check if the videos_watched.json file exists
if os.path.exists(videos_watched_path):
    # Open the videos_watched.json file
    with open(videos_watched_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the topics of interest from the data
        for video in data["impressions_history_videos_watched"]:
            if "string_map_data" in video and "Topic" in video["string_map_data"]:
                topics_of_interest.append(video["string_map_data"]["Topic"]["value"])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])