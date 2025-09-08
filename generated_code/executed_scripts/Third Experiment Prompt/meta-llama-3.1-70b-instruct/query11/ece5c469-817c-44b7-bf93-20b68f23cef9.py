import os
import json
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    viewed_posts = set()
    try:
        with open(os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")) as f:
            data = json.load(f)
            for post in data["likes_media_likes"]:
                for item in post["string_list_data"]:
                    viewed_posts.add(item["href"])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The liked_posts.json file does not exist.")
    return viewed_posts

def get_saved_posts(root_dir):
    saved_posts = set()
    try:
        with open(os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")) as f:
            data = json.load(f)
            for post in data["saved_saved_media"]:
                saved_posts.add(post["string_map_data"]["Saved on"]["href"])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The saved_posts.json file does not exist.")
    return saved_posts

def get_accounts(root_dir):
    viewed_posts = get_viewed_posts(root_dir)
    saved_posts = get_saved_posts(root_dir)
    accounts = set()
    for post in viewed_posts:
        if post not in saved_posts:
            accounts.add(post)
    return accounts

def write_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    accounts = get_accounts(root_dir)
    write_csv(accounts)
except FileNotFoundError as e:
    print(f"Error: {e}")
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])