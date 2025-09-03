import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while reading the file {file_path}: {e}")

def parse_json_content(json_content):
    import json
    try:
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: An error occurred while parsing JSON content: {e}")

def get_following_profiles(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    if not os.path.exists(following_file_path):
        return set()
    
    following_content = get_file_content(following_file_path)
    following_data = parse_json_content(following_content)
    
    following_profiles = set()
    for item in following_data.get("relationships_following", []):
        for data in item.get("string_list_data", []):
            following_profiles.add(data.get("value", ""))
    
    return following_profiles

def get_followers_profiles(root_dir):
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    if not os.path.exists(followers_file_path):
        return set()
    
    followers_content = get_file_content(followers_file_path)
    followers_data = parse_json_content(followers_content)
    
    followers_profiles = set()
    for item in followers_data:
        for data in item.get("string_list_data", []):
            followers_profiles.add(data.get("value", ""))
    
    return followers_profiles

def find_non_mutual_follows(following_profiles, followers_profiles):
    return following_profiles - followers_profiles

def main():
    try:
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        non_mutual_follows = find_non_mutual_follows(following_profiles, followers_profiles)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])
            for profile in non_mutual_follows:
                writer.writerow([profile])
    
    except Exception as e:
        # If any error occurs, create an empty CSV with only the column headers
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Profile'])

if __name__ == "__main__":
    main()