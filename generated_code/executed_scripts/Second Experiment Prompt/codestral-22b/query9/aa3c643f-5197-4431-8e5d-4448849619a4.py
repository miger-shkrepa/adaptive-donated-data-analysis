import os
import json
import csv

root_dir = "root_dir"

def get_following(user_dir):
    following_file = os.path.join(user_dir, "connections", "followers_and_following", "following.json")
    if not os.path.exists(following_file):
        return []
    with open(following_file, 'r') as f:
        data = json.load(f)
    return [item["string_list_data"][0]["value"] for item in data["relationships_following"]]

def get_followers(user_dir):
    followers_file = os.path.join(user_dir, "connections", "followers_and_following", "followers_1.json")
    if not os.path.exists(followers_file):
        return []
    with open(followers_file, 'r') as f:
        data = json.load(f)
    return [item["string_list_data"][0]["value"] for item in data]

def get_unfollowed_profiles(user_dir):
    following = set(get_following(user_dir))
    followers = set(get_followers(user_dir))
    return list(following - followers)

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    results = []
    for user in os.listdir(root_dir):
        user_dir = os.path.join(root_dir, user)
        if os.path.isdir(user_dir):
            unfollowed_profiles = get_unfollowed_profiles(user_dir)
            results.extend(unfollowed_profiles)

    with open('query_responses/results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Profile"])
        for profile in results:
            writer.writerow([profile])

if __name__ == "__main__":
    main()