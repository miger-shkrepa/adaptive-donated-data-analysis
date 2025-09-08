import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Initialize variables to store the counts
post_views = {}
video_views = {}

# Load the posts viewed data
try:
    with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json"), "r") as f:
        posts_data = json.load(f)
except FileNotFoundError:
    print("Error: posts_viewed.json not found. Treating as 0.")
    posts_data = []

# Load the videos watched data
try:
    with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json"), "r") as f:
        videos_data = json.load(f)
except FileNotFoundError:
    print("Error: videos_watched.json not found. Treating as 0.")
    videos_data = []

# Count the post views
for post in posts_data:
    if isinstance(post, dict) and "impressions_history_posts_seen" in post:
        for item in post["impressions_history_posts_seen"]:
            if isinstance(item, dict) and "string_map_data" in item:
                author = item["string_map_data"].get("Author", {}).get("value")
                if author:
                    if author not in post_views:
                        post_views[author] = 0
                    post_views[author] += 1

# Count the video views
for video in videos_data:
    if isinstance(video, dict) and "impressions_history_videos_watched" in video:
        for item in video["impressions_history_videos_watched"]:
            if isinstance(item, dict) and "string_map_data" in item:
                author = item["string_map_data"].get("Author", {}).get("value")
                if author:
                    if author not in video_views:
                        video_views[author] = 0
                    video_views[author] += 1

# Create the CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])
    for author in set(list(post_views.keys()) + list(video_views.keys())):
        post_view_count = post_views.get(author, 0)
        video_view_count = video_views.get(author, 0)
        writer.writerow([author, post_view_count, video_view_count])