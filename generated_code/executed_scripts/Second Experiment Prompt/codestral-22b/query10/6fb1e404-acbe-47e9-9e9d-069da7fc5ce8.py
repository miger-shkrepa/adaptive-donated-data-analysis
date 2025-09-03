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
        views = {}
        for item in data[key]:
            if "Author" in item["string_map_data"]:
                author = item["string_map_data"]["Author"]["value"]
                if author in views:
                    views[author] += 1
                else:
                    views[author] = 1
        return views
    else:
        return {}

# Count views from each data structure
ads_views = count_views(ads_viewed_data, "impressions_history_ads_seen")
video_views = count_views(videos_watched_data, "impressions_history_videos_watched")
post_views = count_views(posts_viewed_data, "impressions_history_posts_seen")

# Combine the views from all data structures
all_views = {}
for views in [ads_views, video_views, post_views]:
    for account, count in views.items():
        if account in all_views:
            all_views[account] += count
        else:
            all_views[account] = count

# Convert the combined views to a list of dictionaries
for account, views in all_views.items():
    results.append({"Account": account, "Post Views": post_views.get(account, 0), "Video Views": video_views.get(account, 0)})

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
    writer.writeheader()
    writer.writerows(results)