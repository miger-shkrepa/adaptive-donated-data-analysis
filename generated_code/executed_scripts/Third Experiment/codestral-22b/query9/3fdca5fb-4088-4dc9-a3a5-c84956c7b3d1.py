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
followers_file = os.path.join(root_dir, "connections", "followers_and_following", "followers_1.json")
following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")

# Check if the followers and following files exist
if not os.path.exists(followers_file):
    raise FileNotFoundError("FileNotFoundError: The followers file does not exist.")
if not os.path.exists(following_file):
    raise FileNotFoundError("FileNotFoundError: The following file does not exist.")

# Load the followers and following data
with open(followers_file, 'r') as f:
    followers_data = json.load(f)
with open(following_file, 'r') as f:
    following_data = json.load(f)

# Extract the followers and following usernames
followers = [item['value'] for item in followers_data[0]['string_list_data']]
following = [item['value'] for item in following_data['relationships_following'][0]['string_list_data']]

# Find the profiles that the user follows but do not follow back
unfollowed_profiles = [profile for profile in following if profile not in followers]

# Add the unfollowed profiles to the list
profiles.extend(unfollowed_profiles)

# Save the results to a CSV file
output_file = "query_responses/results.csv"
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])

print("Results saved to:", output_file)