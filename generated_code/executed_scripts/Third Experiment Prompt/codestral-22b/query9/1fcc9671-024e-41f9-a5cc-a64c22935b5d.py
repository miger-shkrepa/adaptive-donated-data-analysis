import os
import json
import csv

root_dir = "root_dir"

def get_following_and_followers(root_dir):
    following = set()
    followers = set()

    connections_dir = os.path.join(root_dir, "connections", "followers_and_following")

    if not os.path.exists(connections_dir):
        raise FileNotFoundError("FileNotFoundError: The connections directory does not exist.")

    following_file = os.path.join(connections_dir, "following.json")
    followers_file = os.path.join(connections_dir, "followers_1.json")

    try:
        with open(following_file, 'r') as f:
            data = json.load(f)
            for user in data["relationships_following"]:
                following.add(user["title"])
    except FileNotFoundError:
        print("Warning: The following.json file does not exist.")

    try:
        with open(followers_file, 'r') as f:
            data = json.load(f)
            for user in data:
                followers.add(user["title"])
    except FileNotFoundError:
        print("Warning: The followers_1.json file does not exist.")

    return following, followers

def get_unfollowed_profiles(following, followers):
    unfollowed_profiles = following - followers
    return unfollowed_profiles

def save_to_csv(unfollowed_profiles):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in unfollowed_profiles:
            writer.writerow([profile])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    following, followers = get_following_and_followers(root_dir)
    unfollowed_profiles = get_unfollowed_profiles(following, followers)
    save_to_csv(unfollowed_profiles)

if __name__ == "__main__":
    main()