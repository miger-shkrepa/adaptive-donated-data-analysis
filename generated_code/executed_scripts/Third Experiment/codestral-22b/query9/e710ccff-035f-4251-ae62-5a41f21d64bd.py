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

# Define the path to the following.json file
following_path = os.path.join(root_dir, "logged_information", "followers_and_following", "following.json")

# Check if the following.json file exists
if os.path.exists(following_path):
    # Load the following.json file
    with open(following_path, 'r') as f:
        following_data = json.load(f)

    # Extract the profiles the user follows
    following_profiles = [item["value"] for item in following_data["structure"]["relationships_following"][0]["string_list_data"]]

    # Define the path to the followers_1.json file
    followers_path = os.path.join(root_dir, "logged_information", "followers_and_following", "followers_1.json")

    # Check if the followers_1.json file exists
    if os.path.exists(followers_path):
        # Load the followers_1.json file
        with open(followers_path, 'r') as f:
            followers_data = json.load(f)

        # Extract the profiles that follow the user
        followers_profiles = [item["value"] for item in followers_data["structure"][0]["string_list_data"]]

        # Find the profiles the user follows that do not follow him back
        profiles = [profile for profile in following_profiles if profile not in followers_profiles]

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])