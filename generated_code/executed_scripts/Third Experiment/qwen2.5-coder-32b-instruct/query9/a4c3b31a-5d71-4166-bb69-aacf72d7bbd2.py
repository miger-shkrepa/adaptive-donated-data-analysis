import os
import csv

root_dir = "root_dir"

def get_profiles_following(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(following_file_path):
        raise FileNotFoundError("FileNotFoundError: The following.json file does not exist.")
    
    if not os.path.exists(followers_file_path):
        raise FileNotFoundError("FileNotFoundError: The followers_1.json file does not exist.")
    
    following_profiles = set()
    followers_profiles = set()

    try:
        with open(following_file_path, 'r') as following_file:
            import json
            following_data = json.load(following_file)
            for item in following_data['relationships_following']:
                following_profiles.add(item['title'])
    except Exception as e:
        raise ValueError(f"ValueError: Error reading following.json file - {str(e)}")

    try:
        with open(followers_file_path, 'r') as followers_file:
            import json
            followers_data = json.load(followers_file)
            for item in followers_data:
                followers_profiles.add(item['title'])
    except Exception as e:
        raise ValueError(f"ValueError: Error reading followers_1.json file - {str(e)}")

    profiles_not_following_back = following_profiles - followers_profiles

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles_not_following_back:
            writer.writerow([profile])
