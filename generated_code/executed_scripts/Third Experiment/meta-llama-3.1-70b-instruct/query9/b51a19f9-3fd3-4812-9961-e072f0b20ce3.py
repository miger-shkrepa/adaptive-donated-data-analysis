import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    try:
        following_file = os.path.join(root_dir, "recently_unfollowed_profiles.json")
        if not os.path.exists(following_file):
            raise FileNotFoundError("FileNotFoundError: The recently_unfollowed_profiles.json file does not exist.")
        with open(following_file, 'r') as f:
            following_data = json.load(f)
            following_profiles = [item["string_list_data"][0]["value"] for item in following_data["relationships_unfollowed_users"]]
            return following_profiles
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_followers_profiles(root_dir):
    try:
        followers_file = os.path.join(root_dir, "follow_requests_you've_received.json")
        if not os.path.exists(followers_file):
            raise FileNotFoundError("FileNotFoundError: The follow_requests_you've_received.json file does not exist.")
        with open(followers_file, 'r') as f:
            followers_data = json.load(f)
            followers_profiles = [item["string_list_data"][0]["value"] for item in followers_data["relationships_follow_requests_received"]]
            return followers_profiles
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_profiles_not_following_back(root_dir):
    try:
        following_profiles = get_following_profiles(root_dir)
        followers_profiles = get_followers_profiles(root_dir)
        profiles_not_following_back = [profile for profile in following_profiles if profile not in followers_profiles]
        return profiles_not_following_back
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(profiles, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Profile']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for profile in profiles:
                writer.writerow({'Profile': profile})
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        profiles_not_following_back = get_profiles_not_following_back(root_dir)
        save_to_csv(profiles_not_following_back, 'query_responses/results.csv')
    except Exception as e:
        if "FileNotFoundError" in str(e):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Profile']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        else:
            raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()