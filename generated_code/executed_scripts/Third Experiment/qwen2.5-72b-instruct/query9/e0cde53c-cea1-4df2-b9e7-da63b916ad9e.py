import os
import json
import csv

root_dir = "root_dir"

def get_following_profiles():
    following_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    try:
        with open(following_path, 'r') as file:
            data = json.load(file)
            following_profiles = set(item["string_list_data"][0]["value"] for item in data["relationships_following"])
            return following_profiles
    except FileNotFoundError:
        raise FileNotFoundError("Error: The following.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The following.json file is not a valid JSON.")

def get_followers_profiles():
    followers_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
    try:
        with open(followers_path, 'r') as file:
            data = json.load(file)
            followers_profiles = set(item["string_list_data"][0]["value"] for item in data)
            return followers_profiles
    except FileNotFoundError:
        raise FileNotFoundError("Error: The followers_1.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The followers_1.json file is not a valid JSON.")

def find_non_mutual_follows():
    try:
        following_profiles = get_following_profiles()
        followers_profiles = get_followers_profiles()
        non_mutual_follows = following_profiles - followers_profiles
        return non_mutual_follows
    except Exception as e:
        print(e)
        return set()

def write_to_csv(profiles):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

try:
    non_mutual_follows = find_non_mutual_follows()
    write_to_csv(non_mutual_follows)
except Exception as e:
    print(f"Error: {e}")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])