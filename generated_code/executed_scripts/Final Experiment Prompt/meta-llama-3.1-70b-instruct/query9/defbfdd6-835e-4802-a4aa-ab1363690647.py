import json
import csv
import os

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file {} does not exist.".format(file_path))
    except json.JSONDecodeError:
        raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))

def get_followed_profiles(following_json):
    followed_profiles = []
    for relationship in following_json.get("relationships_following", []):
        for data in relationship.get("string_list_data", []):
            followed_profiles.append(data.get("value"))
    return followed_profiles

def get_followers(followers_json):
    followers = []
    for data in followers_json:
        for item in data.get("string_list_data", []):
            followers.append(item.get("value"))
    return followers

def main():
    following_file_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    try:
        following_json = load_json_file(following_file_path)
        followers_json = load_json_file(followers_file_path)
    except FileNotFoundError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
        return

    followed_profiles = get_followed_profiles(following_json)
    followers = get_followers(followers_json)

    non_mutual_follows = [profile for profile in followed_profiles if profile not in followers]

    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in non_mutual_follows:
            writer.writerow([profile])

if __name__ == "__main__":
    main()