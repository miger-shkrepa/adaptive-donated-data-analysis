import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

viewed_accounts = set()
liked_accounts = set()

# Extract accounts from posts viewed
posts_viewed_path = os.path.join(root_dir, "logged_information", "recent_searches", "account_searches.json")
if os.path.exists(posts_viewed_path):
    with open(posts_viewed_path, "r") as f:
        data = json.load(f)
        for item in data["searches_user"]:
            if "string_map_data" in item and "Suche" in item["string_map_data"]:
                account = item["string_map_data"]["Suche"]["value"]
                viewed_accounts.add(account)

# Extract accounts from liked posts
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        data = json.load(f)
        for item in data["likes_media_likes"]:
            if "string_list_data" in item:
                for data_item in item["string_list_data"]:
                    if "value" in data_item:
                        account = data_item["value"]
                        liked_accounts.add(account)

# Find accounts that have been viewed but not liked
unliked_accounts = viewed_accounts - liked_accounts

# Write results to CSV
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    for account in unliked_accounts:
        writer.writerow([account])