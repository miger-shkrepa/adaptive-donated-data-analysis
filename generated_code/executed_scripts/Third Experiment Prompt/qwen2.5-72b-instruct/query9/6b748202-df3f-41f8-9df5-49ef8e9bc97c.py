import os
import json
import csv

root_dir = "root_dir"

def get_following_and_followers(root_dir):
    following = set()
    followers = set()
    
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Assuming the following and followers data would be in a similar structure
        following_file = os.path.join(root_dir, "your_instagram_activity", "following", "following.json")
        followers_file = os.path.join(root_dir, "your_instagram_activity", "followers", "followers.json")
        
        if os.path.exists(following_file):
            with open(following_file, 'r') as f:
                following_data = json.load(f)
                for entry in following_data.get("following", []):
                    following.add(entry.get("value"))
        
        if os.path.exists(followers_file):
            with open(followers_file, 'r') as f:
                followers_data = json.load(f)
                for entry in followers_data.get("followers", []):
                    followers.add(entry.get("value"))
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise ValueError(f"Error: Unexpected error - {e}")
    
    return following, followers

def find_non_mutual_follows(following, followers):
    non_mutual_follows = following - followers
    return non_mutual_follows

def save_to_csv(profiles, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
            for profile in profiles:
                writer.writerow([profile])
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV - {e}")

def main():
    try:
        following, followers = get_following_and_followers(root_dir)
        non_mutual_follows = find_non_mutual_follows(following, followers)
        save_to_csv(non_mutual_follows, 'query_responses/results.csv')
    except Exception as e:
        print(e)
        # If any error occurs, create an empty CSV with just the header
        save_to_csv([], 'query_responses/results.csv')

if __name__ == "__main__":
    main()