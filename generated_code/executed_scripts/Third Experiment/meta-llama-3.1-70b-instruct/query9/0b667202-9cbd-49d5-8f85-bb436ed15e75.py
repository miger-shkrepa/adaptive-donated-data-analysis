import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    try:
        following_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
        if not os.path.exists(following_path):
            raise FileNotFoundError("FileNotFoundError: The following.json file does not exist.")
        with open(following_path, 'r') as f:
            following_data = json.load(f)
            following_profiles = [profile["string_list_data"][0]["value"] for profile in following_data["relationships_following"]]
            return following_profiles
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_followers_profiles(root_dir):
    try:
        followers_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
        if not os.path.exists(followers_path):
            raise FileNotFoundError("FileNotFoundError: The followers_1.json file does not exist.")
        with open(followers_path, 'r') as f:
            followers_data = json.load(f)
            followers_profiles = [profile["string_list_data"][0]["value"] for profile in followers_data]
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

def save_to_csv(profiles, csv_path):
    try:
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Profile"])
            for profile in profiles:
                writer.writerow([profile])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        profiles_not_following_back = get_profiles_not_following_back(root_dir)
        csv_path = 'query_responses/results.csv'
        save_to_csv(profiles_not_following_back, csv_path)
    except Exception as e:
        print("Error: " + str(e))
        csv_path = 'query_responses/results.csv'
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Profile"])

if __name__ == "__main__":
    main()