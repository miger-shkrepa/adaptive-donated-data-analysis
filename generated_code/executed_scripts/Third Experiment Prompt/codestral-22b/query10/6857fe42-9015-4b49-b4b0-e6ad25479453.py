import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Iterate over all directories in the root directory
for account_dir in os.listdir(root_dir):
    account_path = os.path.join(root_dir, account_dir)

    # Check if the account directory exists
    if not os.path.isdir(account_path):
        continue

    # Initialize post and video views
    post_views = 0
    video_views = 0

    # Check if the posts_viewed.json file exists
    posts_viewed_path = os.path.join(account_path, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(posts_viewed_path):
        with open(posts_viewed_path, "r") as f:
            data = json.load(f)
            post_views = len(data["impressions_history_posts_seen"])

    # Check if the videos_watched.json file exists
    videos_watched_path = os.path.join(account_path, "ads_information", "ads_and_topics", "videos_watched.json")
    if os.path.exists(videos_watched_path):
        with open(videos_watched_path, "r") as f:
            data = json.load(f)
            video_views = len(data["impressions_history_videos_watched"])

    results.append({"Account": account_dir, "Post Views": post_views, "Video Views": video_views})

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
    writer.writeheader()
    writer.writerows(results)