import csv
import json

root_dir = "root_dir"

try:
    with open(root_dir + "/ads_information/ads_and_topics/posts_viewed.json", "r") as f:
        posts_viewed = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")

try:
    with open(root_dir + "/ads_information/ads_and_topics/videos_watched.json", "r") as f:
        videos_watched = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The videos_watched.json file does not exist.")

posts_account_views = {}
videos_account_views = {}

for post in posts_viewed["impressions_history_posts_seen"]:
    author = post["string_map_data"]["Author"]["value"]
    if author not in posts_account_views:
        posts_account_views[author] = 0
    posts_account_views[author] += 1

for video in videos_watched["impressions_history_videos_watched"]:
    author = video["string_map_data"]["Author"]["value"]
    if author not in videos_account_views:
        videos_account_views[author] = 0
    videos_account_views[author] += 1

with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])
    for account in set(list(posts_account_views.keys()) + list(videos_account_views.keys())):
        post_views = posts_account_views.get(account, 0)
        video_views = videos_account_views.get(account, 0)
        writer.writerow([account, post_views, video_views])