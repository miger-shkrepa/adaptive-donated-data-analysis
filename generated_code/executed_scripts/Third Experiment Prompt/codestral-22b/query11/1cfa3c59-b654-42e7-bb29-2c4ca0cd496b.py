import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

viewed_posts = set()
liked_posts = set()

# Traverse the directory to find the relevant JSON files
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "posts_viewed.json":
            try:
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = json.load(f)
                    for post in data["impressions_history_posts_seen"]:
                        if "Author" in post["string_map_data"]:
                            viewed_posts.add(post["string_map_data"]["Author"]["value"])
            except Exception as e:
                print(f"Error: {e}")
        elif filename == "liked_posts.json":
            try:
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = json.load(f)
                    for post in data["likes_media_likes"]:
                        for like in post["string_list_data"]:
                            liked_posts.add(like["value"])
            except Exception as e:
                print(f"Error: {e}")

# Find the accounts that the user has viewed posts from but not liked
unliked_posts = viewed_posts - liked_posts

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    for account in unliked_posts:
        writer.writerow([account])