import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
story_likes_file = os.path.join(root_dir, "story_activities", "story_likes.json")

if not os.path.exists(posts_viewed_file):
    print("Warning: posts_viewed.json not found. Skipping this part of the query.")
    posts_viewed = []
else:
    with open(posts_viewed_file, 'r') as f:
        posts_viewed = json.load(f)["impressions_history_posts_seen"]

if not os.path.exists(story_likes_file):
    print("Warning: story_likes.json not found. Assuming no likes.")
    story_likes = []
else:
    with open(story_likes_file, 'r') as f:
        story_likes = json.load(f)["story_activities_story_likes"]

liked_accounts = {like["title"] for like in story_likes}
viewed_accounts = {post["string_map_data"]["Author"]["value"] for post in posts_viewed}

unliked_accounts = viewed_accounts - liked_accounts

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    for account in unliked_accounts:
        writer.writerow([account])