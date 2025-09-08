import json
import os
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_followed_profiles(following_data):
    followed_profiles = set()
    for entry in following_data.get("relationships_following", []):
        for string_data in entry.get("string_list_data", []):
            followed_profiles.add(string_data.get("value"))
    return followed_profiles

def get_follower_profiles(followers_data):
    follower_profiles = set()
    for entry in followers_data.get("string_list_data", []):
        follower_profiles.add(entry.get("value"))
    return follower_profiles

def find_non_mutual_follows(followed_profiles, follower_profiles):
    return followed_profiles - follower_profiles

def save_to_csv(profiles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

def main():
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    output_file = "query_responses/results.csv"

    followed_profiles = set()
    follower_profiles = set()

    try:
        if os.path.exists(following_file):
            following_data = load_json_data(following_file)
            followed_profiles = get_followed_profiles(following_data)
        else:
            print("Warning: following.json not found. Assuming no followed profiles.")

        if os.path.exists(followers_file):
            followers_data = load_json_data(followers_file)
            follower_profiles = get_follower_profiles(followers_data)
        else:
            print("Warning: followers_1.json not found. Assuming no follower profiles.")

        non_mutual_follows = find_non_mutual_follows(followed_profiles, follower_profiles)
        save_to_csv(non_mutual_follows, output_file)
    except Exception as e:
        print(f"Error: {e}")
        save_to_csv([], output_file)

if __name__ == "__main__":
    main()