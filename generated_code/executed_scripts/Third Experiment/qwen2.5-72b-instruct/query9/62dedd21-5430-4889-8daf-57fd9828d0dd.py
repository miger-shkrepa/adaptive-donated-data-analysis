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
    following_file_path = os.path.join(root_dir, "followers_and_following", "following.json")
    if not os.path.exists(following_file_path):
        return []
    following_data = load_json_data(following_file_path)
    following_profiles = [item['string_list_data'][0]['value'] for item in following_data['relationships_following']]
    return following_profiles

def get_follower_profiles():
    followers_file_path = os.path.join(root_dir, "followers_and_following", "followers_1.json")
    if not os.path.exists(followers_file_path):
        return []
    followers_data = load_json_data(followers_file_path)
    follower_profiles = [item['string_list_data'][0]['value'] for item in followers_data['string_list_data']]
    return follower_profiles

def find_non_mutual_follows():
    following_profiles = get_following_profiles()
    follower_profiles = get_follower_profiles()
    non_mutual_follows = [profile for profile in following_profiles if profile not in follower_profiles]
    return non_mutual_follows

def write_to_csv(profiles):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    non_mutual_follows = find_non_mutual_follows()
    write_to_csv(non_mutual_follows)
except Exception as e:
    print(e)