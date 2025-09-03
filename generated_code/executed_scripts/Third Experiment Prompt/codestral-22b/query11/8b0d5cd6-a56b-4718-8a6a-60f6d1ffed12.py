import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

viewed_posts = set()
liked_posts = set()

# Traverse the directory to find the posts viewed and liked
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == "posts_viewed.json":
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for post in data["impressions_history_posts_seen"]:
                        if "Author" in post["string_map_data"]:
                            viewed_posts.add(post["string_map_data"]["Author"]["value"])
            except Exception as e:
                print(f"Error: {e}")
        elif file == "liked_posts.json":
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for post in data["likes_media_likes"]:
                        if "string_list_data" in post:
                            for item in post["string_list_data"]:
                                if "value" in item:
                                    liked_posts.add(item["value"])
            except Exception as e:
                print(f"Error: {e}")

# Find the accounts that have been viewed but not liked
unliked_posts = viewed_posts - liked_posts

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    for account in unliked_posts:
        writer.writerow([account])