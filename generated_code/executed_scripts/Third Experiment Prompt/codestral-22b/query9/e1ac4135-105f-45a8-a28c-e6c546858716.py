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
                following.add(item["string_list_data"][0]["value"])
    return following

def get_followers(user_dir):
    followers = set()
    followers_file = os.path.join(user_dir, "connections", "followers_and_following", "followers_1.json")
    if os.path.exists(followers_file):
        with open(followers_file, 'r') as f:
            data = json.load(f)
            for item in data:
                followers.add(item["string_list_data"][0]["value"])
    return followers

def get_unfollowed_profiles(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    following = get_following(root_dir)
    followers = get_followers(root_dir)

    unfollowed_profiles = following - followers
    return list(unfollowed_profiles)

def save_results(unfollowed_profiles):
    output_dir = "query_responses"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "results.csv")
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Profile"])
        for profile in unfollowed_profiles:
            writer.writerow([profile])

try:
    unfollowed_profiles = get_unfollowed_profiles(root_dir)
    save_results(unfollowed_profiles)
except Exception as e:
    print(f"Error: {str(e)}")