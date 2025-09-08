import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    try:
        following_file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if not os.path.exists(following_file_path):
            raise FileNotFoundError("FileNotFoundError: The liked_posts.json file does not exist.")
        
        with open(following_file_path, "r") as following_file:
            following_data = json.load(following_file)
            following_profiles = [item["title"] for item in following_data["likes_media_likes"]]
            return following_profiles
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_followers_profiles(root_dir):
    try:
        followers_file_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        if not os.path.exists(followers_file_path):
            raise FileNotFoundError("FileNotFoundError: The saved_posts.json file does not exist.")
        
        with open(followers_file_path, "r") as followers_file:
            followers_data = json.load(followers_file)
            followers_profiles = [item["title"] for item in followers_data["saved_saved_media"]]
            return followers_profiles
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_profiles_not_following_back(root_dir):
    try:
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        
        if following_profiles is None or followers_profiles is None:
            return []
        
        profiles_not_following_back = [profile for profile in following_profiles if profile not in followers_profiles]
        return profiles_not_following_back
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(root_dir, profiles):
    try:
        csv_file_path = "query_responses/results.csv"
        with open(csv_file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Profile"])
            for profile in profiles:
                csv_writer.writerow([profile])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        profiles_not_following_back = get_profiles_not_following_back(root_dir)
        write_to_csv(root_dir, profiles_not_following_back)
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()