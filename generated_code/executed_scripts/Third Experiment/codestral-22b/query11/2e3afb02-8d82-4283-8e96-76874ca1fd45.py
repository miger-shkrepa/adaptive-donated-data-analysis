import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

accounts_viewed = set()
accounts_liked = set()

# Extract accounts from posts_viewed.json
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
if os.path.exists(posts_viewed_path):
    with open(posts_viewed_path, 'r') as file:
        data = json.load(file)
        for post in data["impressions_history_posts_seen"]:
            accounts_viewed.add(post["string_map_data"]["Author"]["value"])

# Extract accounts from likes.json
likes_path = os.path.join(root_dir, "likes.json")
if os.path.exists(likes_path):
    with open(likes_path, 'r') as file:
        data = json.load(file)
        for like in data:
            accounts_liked.add(like["string_map_data"]["Author"]["value"])

accounts_viewed_not_liked = accounts_viewed - accounts_liked

# Save results to CSV
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Account"])
    for account in accounts_viewed_not_liked:
        writer.writerow([account])