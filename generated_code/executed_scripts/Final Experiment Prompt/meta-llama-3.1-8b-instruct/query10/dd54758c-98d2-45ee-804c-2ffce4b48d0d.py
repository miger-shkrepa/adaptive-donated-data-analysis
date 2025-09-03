import csv
import json

root_dir = "root_dir"

try:
    with open(root_dir + "/ads_information/ads_and_topics/posts_viewed.json", 'r') as f:
        posts_viewed = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")

try:
    with open(root_dir + "/ads_information/ads_and_topics/videos_watched.json", 'r') as f:
        videos_watched = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The videos_watched.json file does not exist.")

# Initialize counters
post_views = {}
video_views = {}

# Count post views
for post in posts_viewed["impressions_history_posts_seen"]:
    author = post["string_map_data"]["Author"]["value"]
    if author not in post_views:
        post_views[author] = 0
    post_views[author] += 1

# Count video views
for video in videos_watched["impressions_history_videos_watched"]:
    author = video["string_map_data"]["Author"]["value"]
    if author not in video_views:
        video_views[author] = 0
    video_views[author] += 1

# Create CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Write results
    for author in set(list(post_views.keys()) + list(video_views.keys())):
        post_view_count = post_views.get(author, 0)
        video_view_count = video_views.get(author, 0)
        writer.writerow([author, post_view_count, video_view_count])