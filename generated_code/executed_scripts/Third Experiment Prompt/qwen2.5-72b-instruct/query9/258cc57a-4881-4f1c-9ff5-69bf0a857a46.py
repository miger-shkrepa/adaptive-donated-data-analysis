import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def get_following_profiles():
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    if not os.path.exists(following_file_path):
        return []
    following_data = load_json_file(following_file_path)
    following_profiles = [item["string_list_data"][0]["value"] for item in following_data["relationships_following"]]
    return following_profiles

def get_followers_profiles():
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    if not os.path.exists(followers_file_path):
        return []
    followers_data = load_json_file(followers_file_path)
    followers_profiles = [item["string_list_data"][0]["value"] for item in followers_data]
    return followers_profiles

def find_non_mutual_follows():
    following_profiles = get_following_profiles()
    followers_profiles = get_followers_profiles()
    
    non_mutual_follows = [profile for profile in following_profiles if profile not in followers_profiles]
    return non_mutual_follows

def save_to_csv(profiles):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        non_mutual_follows = find_non_mutual_follows()
        save_to_csv(non_mutual_follows)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()