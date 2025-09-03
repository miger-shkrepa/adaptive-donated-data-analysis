import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_profiles(json_data, key):
    profiles = set()
    if isinstance(json_data, list):
        for item in json_data:
            for string_data in item.get("string_list_data", []):
                profiles.add(string_data.get("value"))
    else:
        for item in json_data.get(key, []):
            for string_data in item.get("string_list_data", []):
                profiles.add(string_data.get("value"))
    return profiles

def main():
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    try:
        following_data = load_json(following_file)
        followers_data = load_json(followers_file)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
        return

    try:
        following_profiles = extract_profiles(following_data.get("relationships_following", []), None)
        followers_profiles = extract_profiles(followers_data, "string_list_data")
    except ValueError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Profile"])
        return

    non_followers = following_profiles - followers_profiles

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in non_followers:
            writer.writerow([profile])

if __name__ == "__main__":
    main()