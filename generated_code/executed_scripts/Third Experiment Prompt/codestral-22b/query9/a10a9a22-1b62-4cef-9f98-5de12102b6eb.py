import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize lists to store followers and following
followers = []
following = []

# Load followers data
followers_file = os.path.join(root_dir, "followers.json")
if os.path.exists(followers_file):
    with open(followers_file, 'r') as f:
        followers = json.load(f)

# Load following data
following_file = os.path.join(root_dir, "following.json")
if os.path.exists(following_file):
    with open(following_file, 'r') as f:
        following = json.load(f)

# Find profiles that the user follows but do not follow back
not_following_back = [profile for profile in following if profile not in followers]

# Write the results to a CSV file
output_file = "query_responses/results.csv"
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    for profile in not_following_back:
        writer.writerow([profile])