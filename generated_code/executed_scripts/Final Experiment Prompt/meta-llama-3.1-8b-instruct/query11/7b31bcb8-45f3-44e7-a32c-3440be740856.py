import csv
import json

root_dir = "root_dir"

try:
    with open(f"{root_dir}/ads_information/ads_and_topics/posts_viewed.json", "r") as f:
        posts_viewed = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")

try:
    with open(f"{root_dir}/your_instagram_activity/likes/liked_posts.json", "r") as f:
        liked_posts = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The liked_posts.json file does not exist.")

accounts_viewed = set()
for post in posts_viewed["impressions_history_posts_seen"]:
    accounts_viewed.add(post["string_map_data"]["Author"]["value"])

accounts_liked = set()
for post in liked_posts.get("likes_media_likes", []):
    if "title" in post:
        accounts_liked.add(post["title"])

accounts_viewed_but_not_liked = accounts_viewed - accounts_liked

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # header
    for account in accounts_viewed_but_not_liked:
        writer.writerow([account])