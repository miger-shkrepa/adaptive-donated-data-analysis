import os
import json
import csv

root_dir = "root_dir"

def get_accounts(root_dir):
    accounts = set()
    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, "r") as f:
                posts_viewed_data = json.load(f)
                for post in posts_viewed_data["impressions_history_posts_seen"]:
                    accounts.add(post["string_map_data"]["Author"]["value"])
        else:
            raise FileNotFoundError("FileNotFoundError: posts_viewed.json does not exist.")
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

    try:
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, "r") as f:
                liked_posts_data = json.load(f)
                liked_accounts = set()
                for post in liked_posts_data["likes_media_likes"]:
                    liked_accounts.add(post["string_list_data"][0]["value"])
                accounts = accounts - liked_accounts
        else:
            raise FileNotFoundError("FileNotFoundError: liked_posts.json does not exist.")
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

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
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
    print("Error: " + str(e))