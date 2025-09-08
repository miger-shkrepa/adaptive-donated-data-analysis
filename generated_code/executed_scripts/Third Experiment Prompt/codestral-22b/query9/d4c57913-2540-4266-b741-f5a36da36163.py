import os
import json
import csv

root_dir = "root_dir"

def get_user_following(root_dir):
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    try:
        with open(following_file, 'r') as f:
            following_data = json.load(f)
            return set([item["title"] for item in following_data["relationships_following"]])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The following.json file does not exist.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def get_user_followers(root_dir):
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    try:
        with open(followers_file, 'r') as f:
            followers_data = json.load(f)
            return set([item["title"] for item in followers_data])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The followers_1.json file does not exist.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def get_unfollowed_profiles(root_dir):
    try:
        following = get_user_following(root_dir)
        followers = get_user_followers(root_dir)
        unfollowed_profiles = following - followers
        return list(unfollowed_profiles)
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Profile"])
        for profile in data:
            writer.writerow([profile])

try:
    unfollowed_profiles = get_unfollowed_profiles(root_dir)
    save_to_csv(unfollowed_profiles, "query_responses/results.csv")
except Exception as e:
    print(str(e))