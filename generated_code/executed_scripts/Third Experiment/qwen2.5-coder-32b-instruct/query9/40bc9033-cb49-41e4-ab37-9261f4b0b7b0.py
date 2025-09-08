import os
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
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
            for item in following_data.get('relationships_following', []):
                for data in item.get('string_list_data', []):
                    following_profiles.add(data.get('value', ''))
    except Exception as e:
        raise ValueError(f"ValueError: Error reading following.json - {str(e)}")

    try:
        with open(followers_file_path, 'r') as followers_file:
            import json
            followers_data = json.load(followers_file)
            for item in followers_data:
                for data in item.get('string_list_data', []):
                    followers_profiles.add(data.get('value', ''))
    except Exception as e:
        raise ValueError(f"ValueError: Error reading followers_1.json - {str(e)}")

    non_mutual_follows = following_profiles - followers_profiles

    return non_mutual_follows

def save_to_csv(profiles, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
            for profile in profiles:
                writer.writerow([profile])
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to CSV - {str(e)}")

try:
    non_mutual_follows = get_following_profiles(root_dir)
    save_to_csv(non_mutual_follows, 'query_responses/results.csv')
except Exception as e:
    print(e)
    save_to_csv([], 'query_responses/results.csv')