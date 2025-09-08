import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")

if not os.path.exists(following_file) or not os.path.exists(followers_file):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
    raise FileNotFoundError("FileNotFoundError: Required files for the query do not exist.")

with open(following_file, 'r') as f:
    following_data = json.load(f)

with open(followers_file, 'r') as f:
    followers_data = json.load(f)

following_profiles = set(item["string_list_data"][0]["value"] for item in following_data["relationships_following"])
followers_profiles = set(item["string_list_data"][0]["value"] for item in followers_data)

not_following_back = following_profiles - followers_profiles

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    for profile in not_following_back:
        writer.writerow([profile])