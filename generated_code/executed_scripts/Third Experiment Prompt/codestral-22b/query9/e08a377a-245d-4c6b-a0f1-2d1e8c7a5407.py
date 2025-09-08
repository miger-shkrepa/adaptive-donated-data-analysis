import os
import json
import csv

root_dir = "root_dir"

def get_following(user_data):
    following = set()
    following_path = os.path.join(root_dir, user_data, "connections", "followers_and_following", "following.json")
    if os.path.exists(following_path):
        with open(following_path, 'r') as f:
            data = json.load(f)
            for item in data["relationships_following"]:
                following.add(item["string_list_data"][0]["value"])
    return following

def get_followers(user_data):
    followers = set()
    followers_path = os.path.join(root_dir, user_data, "connections", "followers_and_following", "followers.json")
    if os.path.exists(followers_path):
        with open(followers_path, 'r') as f:
            data = json.load(f)
            for item in data["relationships_followers"]:
                followers.add(item["string_list_data"][0]["value"])
    return followers

def get_unfollowed_profiles(user_data):
    following = get_following(user_data)
    followers = get_followers(user_data)
    return following - followers

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    results = []
    for user_data in os.listdir(root_dir):
        unfollowed_profiles = get_unfollowed_profiles(user_data)
        for profile in unfollowed_profiles:
            results.append({"Profile": profile})

    with open('query_responses/results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Profile"])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()