import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

viewed_posts = set()
liked_posts = set()

# Get viewed posts
viewed_posts_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
if os.path.exists(viewed_posts_path):
    with open(viewed_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["impressions_history_posts_seen"]:
            viewed_posts.add(post["string_map_data"]["Author"]["value"])

# Get liked posts
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["likes_media_likes"]:
            liked_posts.add(post["title"])

# Find accounts with viewed but not liked posts
unliked_posts = viewed_posts - liked_posts

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])
    for account in unliked_posts:
        writer.writerow([account])