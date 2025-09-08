import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

viewed_accounts = set()
liked_accounts = set()

# Extract accounts from posts viewed
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
if os.path.exists(posts_viewed_path):
    with open(posts_viewed_path, "r") as f:
        data = json.load(f)
        for post in data["impressions_history_posts_seen"]:
            viewed_accounts.add(post["string_map_data"]["Author"]["value"])

# Extract accounts from liked posts
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        data = json.load(f)
        for post in data["likes_media_likes"]:
            liked_accounts.add(post["string_list_data"][0]["value"])

# Find accounts that have been viewed but not liked
unliked_accounts = viewed_accounts - liked_accounts

# Write results to CSV
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    for account in unliked_accounts:
        writer.writerow([account])