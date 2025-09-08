import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(directory):
    following_profiles = set()
    following_path = os.path.join(directory, "following", "following.json")
    if not os.path.exists(following_path):
        return following_profiles

    try:
        with open(following_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get("following", []):
                following_profiles.add(entry.get("string_map_data", {}).get("Name", {}).get("value", ""))
    except (json.JSONDecodeError, KeyError):
        raise ValueError("Error: Failed to parse following.json or missing required keys.")
    return following_profiles

def get_followers_profiles(directory):
    followers_profiles = set()
    followers_path = os.path.join(directory, "followers", "followers.json")
    if not os.path.exists(followers_path):
        return followers_profiles

    try:
        with open(followers_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get("followers", []):
                followers_profiles.add(entry.get("string_map_data", {}).get("Name", {}).get("value", ""))
    except (json.JSONDecodeError, KeyError):
        raise ValueError("Error: Failed to parse followers.json or missing required keys.")
    return followers_profiles

def find_non_mutual_follows(directory):
    following = get_following_profiles(directory)
    followers = get_followers_profiles(directory)
    non_mutual_follows = following - followers
    return non_mutual_follows

def write_to_csv(profiles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    try:
        non_mutual_follows = find_non_mutual_follows(root_dir)
        write_to_csv(non_mutual_follows, 'query_responses/results.csv')
    except Exception as e:
        print(f"An error occurred: {e}")