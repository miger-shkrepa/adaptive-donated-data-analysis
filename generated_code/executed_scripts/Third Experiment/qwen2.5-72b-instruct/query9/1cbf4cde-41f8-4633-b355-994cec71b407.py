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
    following_file = os.path.join(root_dir, "personal_information", "following.json")
    try:
        data = load_json_data(following_file)
        following_profiles = [item['string_list_data'][0]['value'] for item in data['relationships_following']]
        return following_profiles
    except FileNotFoundError:
        return []

def get_followers_profiles():
    followers_file = os.path.join(root_dir, "personal_information", "follow_requests_you've_received.json")
    try:
        data = load_json_data(followers_file)
        followers_profiles = [item['string_list_data'][0]['value'] for item in data['relationships_follow_requests_received']]
        return followers_profiles
    except FileNotFoundError:
        return []

def find_non_mutual_follows():
    following = get_following_profiles()
    followers = get_followers_profiles()
    non_mutual_follows = [profile for profile in following if profile not in followers]
    return non_mutual_follows

def write_to_csv(profiles):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

try:
    non_mutual_follows = find_non_mutual_follows()
    write_to_csv(non_mutual_follows)
except Exception as e:
    print(f"An error occurred: {e}")