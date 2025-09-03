import os
import json
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

def get_following_profiles(data):
    following = set()
    if 'relationships_following' in data:
        for entry in data['relationships_following']:
            for string_data in entry['string_list_data']:
                following.add(string_data['value'])
    return following

def get_followers_profiles(data):
    followers = set()
    if 'relationships_feed_favorites' in data:
        for entry in data['relationships_feed_favorites']:
            for string_data in entry['string_list_data']:
                followers.add(string_data['value'])
    return followers

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
        print(f"Error: {e}")
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])

if __name__ == "__main__":
    main()