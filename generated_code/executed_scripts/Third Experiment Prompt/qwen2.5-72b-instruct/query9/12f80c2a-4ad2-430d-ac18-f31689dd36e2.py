import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_following_profiles(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    if not os.path.exists(following_file):
        return []
    data = load_json_file(following_file)
    following_profiles = [item['string_list_data'][0]['value'] for item in data['relationships_following']]
    return following_profiles

def get_followers_profiles(root_dir):
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json")
    if not os.path.exists(followers_file):
        return []
    data = load_json_file(followers_file)
    followers_profiles = [item['string_list_data'][0]['value'] for item in data['relationships_close_friends']]
    return followers_profiles

def find_non_mutual_follows(root_dir):
    following_profiles = get_following_profiles(root_dir)
    followers_profiles = get_followers_profiles(root_dir)
    
    non_mutual_follows = [profile for profile in following_profiles if profile not in followers_profiles]
    return non_mutual_follows

def save_to_csv(profiles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    non_mutual_follows = find_non_mutual_follows(root_dir)
    save_to_csv(non_mutual_follows, 'query_responses/results.csv')

if __name__ == "__main__":
    main()