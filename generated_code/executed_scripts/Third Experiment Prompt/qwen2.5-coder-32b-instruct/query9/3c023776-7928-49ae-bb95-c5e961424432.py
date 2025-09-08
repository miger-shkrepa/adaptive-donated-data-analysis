import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def get_following_profiles(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    following_profiles = set()
    
    if not os.path.exists(following_file_path):
        return following_profiles
    
    try:
        with open(following_file_path, 'r') as file:
            data = eval(file.read())
            for entry in data.get("relationships_following", []):
                for item in entry.get("string_list_data", []):
                    following_profiles.add(item.get("value", ""))
    except Exception as e:
        raise ValueError(f"ValueError: Error reading following.json - {str(e)}")
    
    return following_profiles

def get_follower_profiles(root_dir):
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    follower_profiles = set()
    
    if not os.path.exists(followers_file_path):
        return follower_profiles
    
    try:
        with open(followers_file_path, 'r') as file:
            data = eval(file.read())
            for entry in data:
                for item in entry.get("string_list_data", []):
                    follower_profiles.add(item.get("value", ""))
    except Exception as e:
        raise ValueError(f"ValueError: Error reading followers_1.json - {str(e)}")
    
    return follower_profiles

def find_non_mutual_follows(following_profiles, follower_profiles):
    return following_profiles - follower_profiles

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    following_profiles = get_following_profiles(root_dir)
    follower_profiles = get_follower_profiles(root_dir)
    
    non_mutual_follows = find_non_mutual_follows(following_profiles, follower_profiles)
    
    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in non_mutual_follows:
            writer.writerow([profile])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)