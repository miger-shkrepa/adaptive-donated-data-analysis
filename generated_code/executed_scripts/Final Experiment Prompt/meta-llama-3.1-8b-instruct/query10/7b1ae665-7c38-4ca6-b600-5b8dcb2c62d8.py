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
    # If the videos_watched.json file does not exist, treat its contribution as 0
    videos_watched = {"impressions_history_videos_watched": []}

# Initialize dictionaries to store account views
account_posts_views = {}
account_videos_views = {}

# Process posts viewed data
for post in posts_viewed["impressions_history_posts_seen"]:
    author = post["string_map_data"]["Author"]["value"]
    if author not in account_posts_views:
        account_posts_views[author] = 0
    account_posts_views[author] += 1

# Process videos watched data
for video in videos_watched["impressions_history_videos_watched"]:
    author = video["string_map_data"]["Author"]["value"]
    if author not in account_videos_views:
        account_videos_views[author] = 0
    account_videos_views[author] += 1

# Initialize list to store CSV rows
csv_rows = []

# Get all unique authors
authors = set(list(account_posts_views.keys()) + list(account_videos_views.keys()))

# Create CSV rows
for author in authors:
    post_views = account_posts_views.get(author, 0)
    video_views = account_videos_views.get(author, 0)
    csv_rows.append([author, post_views, video_views])

# Write CSV rows to file
try:
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        writer.writerows(csv_rows)
except Exception as e:
    raise Exception("Error: Unable to write to results.csv file.")