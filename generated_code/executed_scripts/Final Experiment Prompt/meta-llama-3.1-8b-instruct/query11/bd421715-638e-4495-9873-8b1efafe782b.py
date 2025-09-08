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
accounts_liked = set()

for post in posts_viewed.get("impressions_history_posts_seen", []):
    author = post.get("string_map_data", {}).get("Author", {}).get("value")
    if author:
        accounts_viewed.add(author)

for post in liked_posts.get("likes_media_likes", []):
    title = post.get("title")
    if title:
        accounts_liked.add(title)

accounts_viewed_but_not_liked = accounts_viewed - accounts_liked

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # header
    for account in accounts_viewed_but_not_liked:
        writer.writerow([account])