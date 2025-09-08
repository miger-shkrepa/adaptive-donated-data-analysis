import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Define the paths to the relevant JSON files
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Function to extract data from a JSON file
def extract_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    else:
        return None

# Extract data from the JSON files
ads_viewed_data = extract_data(ads_viewed_path)
videos_watched_data = extract_data(videos_watched_path)
posts_viewed_data = extract_data(posts_viewed_path)

# Function to count views from a data structure
def count_views(data, key):
    if data is not None:
        return len(data[key])
    else:
        return 0

# Count views from each account
account_views = {}

# Count views from ads_viewed.json
if ads_viewed_data is not None and "impressions_history_ads_seen" in ads_viewed_data:
    for item in ads_viewed_data["impressions_history_ads_seen"]:
        account = item["string_map_data"]["Author"]["value"]
        if account not in account_views:
            account_views[account] = {"post_views": 0, "video_views": 0}
        account_views[account]["post_views"] += 1

# Count views from videos_watched.json
if videos_watched_data is not None and "impressions_history_videos_watched" in videos_watched_data:
    for item in videos_watched_data["impressions_history_videos_watched"]:
        account = item["string_map_data"]["Author"]["value"]
        if account not in account_views:
            account_views[account] = {"post_views": 0, "video_views": 0}
        account_views[account]["video_views"] += 1

# Count views from posts_viewed.json
if posts_viewed_data is not None and "impressions_history_posts_seen" in posts_viewed_data:
    for item in posts_viewed_data["impressions_history_posts_seen"]:
        account = item["string_map_data"]["Author"]["value"]
        if account not in account_views:
            account_views[account] = {"post_views": 0, "video_views": 0}
        account_views[account]["post_views"] += 1

# Convert the data to a list of dictionaries
for account, views in account_views.items():
    results.append({"Account": account, "Post Views": views["post_views"], "Video Views": views["video_views"]})

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
    writer.writeheader()
    writer.writerows(results)