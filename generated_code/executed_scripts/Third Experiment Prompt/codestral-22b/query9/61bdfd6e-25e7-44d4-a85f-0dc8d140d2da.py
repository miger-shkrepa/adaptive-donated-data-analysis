import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Define the path to the followers and following files
followers_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
following_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")

# Check if the followers file exists
if os.path.exists(followers_path):
    with open(followers_path, 'r') as f:
        followers = json.load(f)
        followers = [item["string_list_data"][0]["value"] for item in followers]
else:
    followers = []

# Check if the following file exists
if os.path.exists(following_path):
    with open(following_path, 'r') as f:
        following = json.load(f)
        following = [item["string_list_data"][0]["value"] for item in following["relationships_following"]]
else:
    following = []

# Find the profiles that the user follows but do not follow back
not_following_back = [profile for profile in following if profile not in followers]

# Add the profiles to the list
profiles.extend(not_following_back)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    for profile in profiles:
        writer.writerow([profile])