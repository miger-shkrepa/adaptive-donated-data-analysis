import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")

def get_following_and_followers_data():
    following = []
    followers = []

    following_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    if os.path.exists(following_path):
        following_data = load_json_data(following_path)
        for entry in following_data["relationships_following"]:
            for item in entry["string_list_data"]:
                following.append(item["value"])

    if os.path.exists(followers_path):
        followers_data = load_json_data(followers_path)
        for entry in followers_data:
            for item in entry["string_list_data"]:
                followers.append(item["value"])

    return following, followers

def find_non_mutual_follows(following, followers):
    non_mutual_follows = [profile for profile in following if profile not in followers]
    return non_mutual_follows

def write_to_csv(profiles):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in profiles:
            writer.writerow([profile])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    following, followers = get_following_and_followers_data()
    non_mutual_follows = find_non_mutual_follows(following, followers)
    write_to_csv(non_mutual_follows)

except Exception as e:
    print(e)