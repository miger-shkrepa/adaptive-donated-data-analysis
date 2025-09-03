import os
import json
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    viewed_posts = set()
    posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(posts_viewed_file):
        with open(posts_viewed_file, "r") as f:
            data = json.load(f)
            for post in data["impressions_history_posts_seen"]:
                viewed_posts.add(post["string_map_data"]["Author"]["value"])
    return viewed_posts

def get_liked_posts(root_dir):
    liked_posts = set()
    liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(liked_posts_file):
        with open(liked_posts_file, "r") as f:
            data = json.load(f)
            for post in data["likes_media_likes"]:
                if "title" in post:
                    liked_posts.add(post["title"])
    return liked_posts

def get_accounts(root_dir):
    viewed_posts = get_viewed_posts(root_dir)
    liked_posts = get_liked_posts(root_dir)
    accounts = viewed_posts - liked_posts
    return accounts

def write_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    accounts = get_accounts(root_dir)
    write_csv(accounts)
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
except Exception as e:
    print(f"Error: {e}")
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])