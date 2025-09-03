import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    if not os.path.exists(following_file_path):
        raise FileNotFoundError("Error: The following.json file does not exist.")
    
    with open(following_file_path, 'r') as f:
        following_data = json.load(f)
    
    following_profiles = [profile["title"] for profile in following_data["relationships_following"]]
    return following_profiles

def get_followers_profiles(root_dir):
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    if not os.path.exists(followers_file_path):
        raise FileNotFoundError("Error: The followers_1.json file does not exist.")
    
    with open(followers_file_path, 'r') as f:
        followers_data = json.load(f)
    
    followers_profiles = [profile["title"] for profile in followers_data]
    return followers_profiles

def get_profiles_not_following_back(root_dir):
    following_profiles = get_following_profiles(root_dir)
    followers_profiles = get_followers_profiles(root_dir)
    
    profiles_not_following_back = [profile for profile in following_profiles if profile not in followers_profiles]
    return profiles_not_following_back

def save_to_csv(profiles):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Profile']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for profile in profiles:
            writer.writerow({'Profile': profile})

try:
    profiles_not_following_back = get_profiles_not_following_back(root_dir)
    save_to_csv(profiles_not_following_back)
except FileNotFoundError as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Profile']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()