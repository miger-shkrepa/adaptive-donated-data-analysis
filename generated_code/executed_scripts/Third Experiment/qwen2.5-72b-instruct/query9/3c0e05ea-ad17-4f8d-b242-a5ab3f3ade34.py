import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_following_profiles():
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    try:
        data = load_json_data(following_file)
        following_profiles = set()
        for entry in data["relationships_following"]:
            for item in entry["string_list_data"]:
                following_profiles.add(item["value"])
        return following_profiles
    except FileNotFoundError:
        return set()

def get_follower_profiles():
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    try:
        data = load_json_data(followers_file)
        follower_profiles = set()
        for entry in data:
            for item in entry["string_list_data"]:
                follower_profiles.add(item["value"])
        return follower_profiles
    except FileNotFoundError:
        return set()

def find_non_mutual_follows():
    following_profiles = get_following_profiles()
    follower_profiles = get_follower_profiles()
    non_mutual_follows = following_profiles - follower_profiles
    return non_mutual_follows

def write_to_csv(profiles):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

try:
    non_mutual_follows = find_non_mutual_follows()
    write_to_csv(non_mutual_follows)
except Exception as e:
    print(f"An error occurred: {e}")