import os
import json
import csv

root_dir = "root_dir"

def get_accounts(root_dir):
    accounts = set()
    posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(posts_viewed_file):
        with open(posts_viewed_file, "r") as f:
            data = json.load(f)
            for post in data["impressions_history_posts_seen"]:
                accounts.add(post["string_map_data"]["Author"]["value"])
    else:
        raise FileNotFoundError("Error: The posts_viewed.json file does not exist.")

    liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(liked_posts_file):
        with open(liked_posts_file, "r") as f:
            data = json.load(f)
            liked_accounts = set()
            for post in data["likes_media_likes"]:
                liked_accounts.add(post["title"])
            accounts = accounts - liked_accounts
    else:
        # If liked_posts.json is missing, treat its contribution as 0 and continue processing
        pass

    return accounts

def write_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    accounts = get_accounts(root_dir)
    write_to_csv(accounts)
except FileNotFoundError as e:
    raise FileNotFoundError(f"Error: {e}")
except Exception as e:
    raise ValueError(f"Error: {e}")