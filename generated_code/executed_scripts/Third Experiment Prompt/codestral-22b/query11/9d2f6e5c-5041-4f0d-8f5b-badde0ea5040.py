import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

viewed_posts = set()
liked_posts = set()

# Get viewed posts
viewed_posts_path = os.path.join(root_dir, "your_instagram_activity", "media", "posts_1.json")
if os.path.exists(viewed_posts_path):
    with open(viewed_posts_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for post in data:
            if 'title' in post:
                viewed_posts.add(post['title'])

# Get liked posts
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for post in data['likes_media_likes']:
            if 'title' in post:
                liked_posts.add(post['title'])

# Find accounts that have viewed posts but not liked them
unliked_posts = viewed_posts - liked_posts

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for post in unliked_posts:
        writer.writerow([post])