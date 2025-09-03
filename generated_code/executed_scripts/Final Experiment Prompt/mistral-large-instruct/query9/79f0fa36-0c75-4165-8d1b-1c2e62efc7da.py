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
    for item in json_data.get(key, []):
        for string_data in item.get("string_list_data", []):
            profiles.add(string_data.get("value"))
    return profiles

def main():
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
    followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

    following_profiles = set()
    followers_profiles = set()

    if os.path.exists(following_file):
        try:
            following_data = load_json(following_file)
            following_profiles = extract_profiles(following_data, "relationships_following")
        except FileNotFoundError as e:
            print(e)

    if os.path.exists(followers_file):
        try:
            followers_data = load_json(followers_file)
            followers_profiles = extract_profiles(followers_data, "string_list_data")
        except FileNotFoundError as e:
            print(e)

    non_reciprocal_follows = following_profiles - followers_profiles

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
        for profile in non_reciprocal_follows:
            writer.writerow([profile])

if __name__ == "__main__":
    main()