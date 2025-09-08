import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

account_views = {}

# Process posts_viewed.json
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
if os.path.exists(posts_viewed_path):
    with open(posts_viewed_path, 'r') as f:
        data = json.load(f)
        for post in data["impressions_history_posts_seen"]:
            author = post["string_map_data"]["Author"]["value"]
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Post Views"] += 1

# Process videos_watched.json
videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
if os.path.exists(videos_watched_path):
    with open(videos_watched_path, 'r') as f:
        data = json.load(f)
        for video in data["impressions_history_videos_watched"]:
            author = video["string_map_data"]["Author"]["value"]
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Video Views"] += 1

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, views in account_views.items():
        writer.writerow({'Account': account, 'Post Views': views["Post Views"], 'Video Views': views["Video Views"]})