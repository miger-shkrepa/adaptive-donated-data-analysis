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

# Define the path to the follow requests JSON file
follow_requests_path = os.path.join(root_dir, "follow_requests_you've_received.json")

# Check if the follow requests JSON file exists
if os.path.exists(follow_requests_path):
    # Open the follow requests JSON file
    with open(follow_requests_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the profiles that the user follows
        followed_profiles = [item['value'] for item in data['relationships_follow_requests_received'][0]['string_list_data']]

        # Define the path to the recently unfollowed profiles JSON file
        unfollowed_profiles_path = os.path.join(root_dir, "recently_unfollowed_profiles.json")

        # Check if the recently unfollowed profiles JSON file exists
        if os.path.exists(unfollowed_profiles_path):
            # Open the recently unfollowed profiles JSON file
            with open(unfollowed_profiles_path, 'r') as f:
                # Load the JSON data
                data = json.load(f)

                # Extract the profiles that do not follow the user back
                unfollowed_profiles = [item['value'] for item in data['relationships_unfollowed_users'][0]['string_list_data']]

                # Find the profiles that the user follows that do not follow him back
                profiles = [profile for profile in followed_profiles if profile in unfollowed_profiles]

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Profile'])
    writer.writerows([[profile] for profile in profiles])