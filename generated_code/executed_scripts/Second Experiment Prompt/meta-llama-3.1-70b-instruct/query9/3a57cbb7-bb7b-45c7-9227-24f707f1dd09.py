import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles(root_dir):
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    try:
        with open(following_file_path, "r") as following_file:
            following_data = json.load(following_file)
            following_profiles = [profile["title"] for profile in following_data["relationships_following"]]
            return following_profiles
    except FileNotFoundError:
        raise FileNotFoundError("Error: The following.json file does not exist.")

def get_followers_profiles(root_dir):
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    try:
        with open(followers_file_path, "r") as followers_file:
            followers_data = json.load(followers_file)
            followers_profiles = [profile["title"] for profile in followers_data]
            return followers_profiles
    except FileNotFoundError:
        raise FileNotFoundError("Error: The followers_1.json file does not exist.")

def get_profiles_not_following_back(root_dir):
    following_profiles = get_following_profiles(root_dir)
    followers_profiles = get_followers_profiles(root_dir)
    profiles_not_following_back = [profile for profile in following_profiles if profile not in followers_profiles]
    return profiles_not_following_back

def write_to_csv(profiles):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

try:
    profiles_not_following_back = get_profiles_not_following_back(root_dir)
    write_to_csv(profiles_not_following_back)
except FileNotFoundError as e:
    print(e)
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])