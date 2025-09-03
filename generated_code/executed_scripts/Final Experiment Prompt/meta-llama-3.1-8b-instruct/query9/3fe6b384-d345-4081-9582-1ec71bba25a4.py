import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Load the following.json file
following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")
try:
    with open(following_file, 'r') as f:
        following_data = json.load(f)
except FileNotFoundError:
    print("Error: The following.json file does not exist.")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
    exit()

# Load the followers_1.json file
followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
try:
    with open(followers_file, 'r') as f:
        followers_data = json.load(f)
except FileNotFoundError:
    print("Error: The followers_1.json file does not exist.")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Profile"])
    exit()

# Extract the list of followed profiles
followed_profiles = []
if 'relationships_following' in following_data and following_data['relationships_following']:
    followed_profiles = [item.get('string_list_data', [{}])[0].get('value', []) for item in following_data['relationships_following']]

# Extract the list of followers
followers = []
if 'string_list_data' in followers_data and followers_data['string_list_data']:
    followers = [item.get('value', []) for item in followers_data['string_list_data']]

# Find the profiles that the user follows but do not follow back
unfollowed_profiles = []
for profile in followed_profiles:
    if isinstance(profile, list):
        unfollowed_profiles.extend(profile)
    else:
        unfollowed_profiles.append(profile)

unfollowed_profiles = [profile for profile in set(unfollowed_profiles) if profile not in followers]

# Save the result to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in unfollowed_profiles])