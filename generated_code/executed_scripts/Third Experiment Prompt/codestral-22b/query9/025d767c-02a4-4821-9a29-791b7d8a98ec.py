import os
import json
import csv

root_dir = "root_dir"

def get_following(user_dir):
    following_file = os.path.join(user_dir, "connections", "followers_and_following", "following.json")
    try:
        with open(following_file, 'r') as f:
            data = json.load(f)
            return [item["string_list_data"][0]["value"] for item in data["relationships_following"]]
    except FileNotFoundError:
        return []

def get_followers(user_dir):
    followers_file = os.path.join(user_dir, "connections", "followers_and_following", "followers_1.json")
    try:
        with open(followers_file, 'r') as f:
            data = json.load(f)
            return [item["string_list_data"][0]["value"] for item in data]
    except FileNotFoundError:
        return []

def get_unfollowed_profiles(user_dir):
    following = set(get_following(user_dir))
    followers = set(get_followers(user_dir))
    return list(following - followers)

def write_to_csv(profiles, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

def main():
    output_file = "query_responses/results.csv"
    try:
        profiles = get_unfollowed_profiles(root_dir)
        write_to_csv(profiles, output_file)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()