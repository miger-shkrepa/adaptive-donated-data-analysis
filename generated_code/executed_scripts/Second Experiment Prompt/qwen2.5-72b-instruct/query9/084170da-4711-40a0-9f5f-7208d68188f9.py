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

def get_following_profiles(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    if not os.path.exists(following_file):
        return []
    data = load_json_file(following_file)
    following_profiles = set()
    for entry in data.get("structure", {}).get("relationships_following", []):
        for item in entry.get("string_list_data", []):
            following_profiles.add(item.get("value"))
    return following_profiles

def get_followers_profiles(root_dir):
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    if not os.path.exists(followers_file):
        return []
    data = load_json_file(followers_file)
    followers_profiles = set()
    for entry in data:  # Iterate over the list directly
        for item in entry.get("string_list_data", []):
            followers_profiles.add(item.get("value"))
    return followers_profiles

def find_non_mutual_follows(root_dir):
    try:
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        
        non_mutual_follows = following_profiles - followers_profiles
        
        return list(non_mutual_follows)
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(profiles, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
            for profile in profiles:
                writer.writerow([profile])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. {str(e)}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        non_mutual_follows = find_non_mutual_follows(root_dir)
        save_to_csv(non_mutual_follows, 'query_responses/results.csv')
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()