import os
import json
import csv

root_dir = "root_dir"

def get_following(user_dir):
    following = set()
    following_file = os.path.join(user_dir, "connections", "followers_and_following", "following.json")
    if os.path.exists(following_file):
        with open(following_file, 'r') as f:
            data = json.load(f)
            for item in data["relationships_following"]:
                following.add(item["title"])
    return following

def get_followers(user_dir):
    followers = set()
    followers_file = os.path.join(user_dir, "connections", "followers_and_following", "followers_1.json")
    if os.path.exists(followers_file):
        with open(followers_file, 'r') as f:
            data = json.load(f)
            for item in data:
                followers.add(item["title"])
    return followers

def get_unfollowed_profiles(root_dir):
    unfollowed_profiles = []
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    following = get_following(root_dir)
    followers = get_followers(root_dir)
    unfollowed_profiles = following - followers
    return unfollowed_profiles

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in data:
            writer.writerow([profile])

unfollowed_profiles = get_unfollowed_profiles(root_dir)
save_to_csv(unfollowed_profiles, "query_responses/results.csv")