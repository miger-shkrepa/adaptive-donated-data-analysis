import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Define the path to the followers and following JSON files
followers_path = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
following_path = os.path.join(root_dir, "connections", "followers_and_following", "following.json")

# Check if the followers and following JSON files exist
if not os.path.exists(followers_path):
    print("Warning: The followers JSON file does not exist. Skipping this part of the analysis.")
    followers = []
else:
    # Load the followers JSON file
    with open(followers_path, "r") as f:
        followers_data = json.load(f)
    # Extract the followers' usernames
    followers = [item["string_list_data"][0]["value"] for item in followers_data]

if not os.path.exists(following_path):
    print("Warning: The following JSON file does not exist. Skipping this part of the analysis.")
    following = []
else:
    # Load the following JSON file
    with open(following_path, "r") as f:
        following_data = json.load(f)
    # Extract the following usernames
    following = [item["string_list_data"][0]["value"] for item in following_data["relationships_following"]]

# Find the profiles that the user follows but do not follow back
unfollowed_profiles = [profile for profile in following if profile not in followers]

# Add the unfollowed profiles to the list
profiles.extend(unfollowed_profiles)

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])