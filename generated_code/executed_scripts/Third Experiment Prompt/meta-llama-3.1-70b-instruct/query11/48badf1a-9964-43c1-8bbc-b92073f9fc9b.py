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
                liked_posts.add(post["string_list_data"][0]["value"])
    return liked_posts

def get_accounts_not_liked(root_dir):
    viewed_posts = get_viewed_posts(root_dir)
    liked_posts = get_liked_posts(root_dir)
    accounts_not_liked = viewed_posts - liked_posts
    return accounts_not_liked

def write_to_csv(accounts_not_liked):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts_not_liked:
            writer.writerow([account])

try:
    accounts_not_liked = get_accounts_not_liked(root_dir)
    write_to_csv(accounts_not_liked)
except FileNotFoundError:
    raise FileNotFoundError("Error: The root directory does not exist.")
except Exception as e:
    raise ValueError("Error: " + str(e))