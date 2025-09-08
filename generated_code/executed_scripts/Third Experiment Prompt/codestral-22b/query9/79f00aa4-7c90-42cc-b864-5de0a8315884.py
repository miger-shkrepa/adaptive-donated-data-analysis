import os
import json
import csv

root_dir = "root_dir"
following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
output_file = "query_responses/results.csv"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_profiles(data):
    profiles = []
    if isinstance(data, list):
        for item in data:
            if "string_list_data" in item:
                for data_item in item["string_list_data"]:
                    if "value" in data_item:
                        profiles.append(data_item["value"])
    return profiles

def get_unfollowed_profiles(following, followers):
    return [profile for profile in following if profile not in followers]

try:
    following_data = load_json(following_file)
    followers_data = load_json(followers_file)

    following_profiles = get_profiles(following_data["relationships_following"])
    followers_profiles = get_profiles(followers_data)

    unfollowed_profiles = get_unfollowed_profiles(following_profiles, followers_profiles)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Profile"])
        for profile in unfollowed_profiles:
            writer.writerow([profile])

except Exception as e:
    print(f"Error: {str(e)}")