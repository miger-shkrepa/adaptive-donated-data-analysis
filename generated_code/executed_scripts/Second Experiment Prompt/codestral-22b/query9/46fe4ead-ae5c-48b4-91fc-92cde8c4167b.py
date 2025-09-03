import os
import json
import csv

root_dir = "root_dir"
following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
output_file = "query_responses/results.csv"

def get_profiles(file_path):
    if not os.path.exists(file_path):
        return set()
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return set(item["string_list_data"][0]["value"] for item in data["relationships_following"])
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

try:
    following = get_profiles(following_file)
    followers = get_profiles(followers_file)
    not_following_back = following - followers

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Profile"])
        for profile in not_following_back:
            writer.writerow([profile])
except Exception as e:
    print(f"Error: {str(e)}")