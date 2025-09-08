import os
import json
import csv

root_dir = "root_dir"

def get_following(user_data):
    following = set()
    try:
        with open(os.path.join(user_data, "connections", "followers_and_following", "following.json")) as f:
            data = json.load(f)
            for user in data["relationships_following"][0]["string_list_data"]:
                following.add(user["value"])
    except FileNotFoundError:
        pass
    return following

def get_followers(user_data):
    followers = set()
    try:
        with open(os.path.join(user_data, "connections", "followers_and_following", "followers_1.json")) as f:
            data = json.load(f)
            for user in data[0]["string_list_data"]:
                followers.add(user["value"])
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

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in data:
            writer.writerow([profile])

try:
    unfollowed_profiles = get_unfollowed_profiles(root_dir)
    save_to_csv(unfollowed_profiles, "query_responses/results.csv")
except Exception as e:
    raise type(e)(f"Error: {str(e)}")