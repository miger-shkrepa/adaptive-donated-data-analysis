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
                    for post in data.get("impressions_history_posts_seen", []):
                        viewed_posts.add(post["string_map_data"]["Author"]["value"])
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        elif filename == "liked_posts.json":
            try:
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = json.load(f)
                    for post in data.get("likes_media_likes", []):
                        liked_posts.add(post["string_list_data"][0]["value"])
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Find the accounts that have been viewed but not liked
unliked_posts = viewed_posts - liked_posts

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])
    for account in unliked_posts:
        writer.writerow([account])