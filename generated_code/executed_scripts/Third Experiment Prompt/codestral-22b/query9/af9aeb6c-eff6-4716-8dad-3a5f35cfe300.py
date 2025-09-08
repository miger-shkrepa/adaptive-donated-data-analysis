import os
import json
import csv

root_dir = "root_dir"

def get_following(user_data):
    following = set()
    try:
        with open(os.path.join(user_data, "connections", "followers_and_following", "following.json")) as f:
            data = json.load(f)
            for user in data["relationships_following"]:
                following.add(user["string_list_data"][0]["value"])
    except FileNotFoundError:
        pass
    return following

def get_followers(user_data):
    followers = set()
    try:
        with open(os.path.join(user_data, "connections", "followers_and_following", "followers_1.json")) as f:
            data = json.load(f)
            for user in data:
                followers.add(user["string_list_data"][0]["value"])
    except FileNotFoundError:
        pass
    return followers

def get_unfollowed_profiles(root_dir):
    unfollowed_profiles = []
    for user_data in os.listdir(root_dir):
        user_path = os.path.join(root_dir, user_data)
        if os.path.isdir(user_path):
            following = get_following(user_path)
            followers = get_followers(user_path)
            unfollowed_profiles.extend(following - followers)
    return unfollowed_profiles

def save_results(unfollowed_profiles):
    with open("query_responses/results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Profile"])
        for profile in unfollowed_profiles:
            writer.writerow([profile])

try:
    unfollowed_profiles = get_unfollowed_profiles(root_dir)
    save_results(unfollowed_profiles)
except Exception as e:
    raise type(e)(f"Error: {str(e)}")