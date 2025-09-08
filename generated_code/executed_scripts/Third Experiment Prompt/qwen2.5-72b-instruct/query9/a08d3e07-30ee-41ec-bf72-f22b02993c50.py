import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")

def get_following_profiles(data):
    following_profiles = set()
    for entry in data.get("relationships_following", []):
        for string_data in entry.get("string_list_data", []):
            following_profiles.add(string_data.get("value"))
    return following_profiles

def get_followers_profiles(data):
    followers_profiles = set()
    for entry in data.get("relationships_feed_favorites", []):
        for string_data in entry.get("string_list_data", []):
            followers_profiles.add(string_data.get("value"))
    return followers_profiles

def find_non_mutual_follows(following, followers):
    return following - followers

def main():
    try:
        following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
        followers_file = os.path.join(root_dir, "connections", "followers_and_following", "accounts_you've_favorited.json")

        following_data = load_json_data(following_file) if os.path.exists(following_file) else {}
        followers_data = load_json_data(followers_file) if os.path.exists(followers_file) else {}

        following_profiles = get_following_profiles(following_data)
        followers_profiles = get_followers_profiles(followers_data)

        non_mutual_follows = find_non_mutual_follows(following_profiles, followers_profiles)

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
            for profile in non_mutual_follows:
                writer.writerow([profile])

    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
    except Exception as e:
        print(f"Error: {str(e)}")
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])

if __name__ == "__main__":
    main()