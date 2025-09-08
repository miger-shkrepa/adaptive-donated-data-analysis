import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the followers_and_following directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
            # Check if the following.json file exists
            if "following.json" in filenames:
                # Open the following.json file
                with open(os.path.join(root_dir, "connections", "followers_and_following", "following.json"), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the data has a 'structure' key
                    if 'structure' in data:
                        # Iterate over the relationships_following list
                        for item in data.get('structure', {}).get('relationships_following', []):
                            # Extract the title (profile name)
                            profile = item.get('title')
                            # Iterate over the relationships_follow_requests_received list
                            for item in data.get('structure', {}).get('relationships_follow_requests_received', []):
                                # Check if the profile is in the list
                                if profile not in [item.get('title') for item in item.get('string_list_data', [])]:
                                    # If the profile is not in the list, add it to the profiles list
                                    profiles.append(profile)
            # Check if the follow_requests_you've_received.json file exists
            elif "follow_requests_you've_received.json" in filenames:
                # Open the follow_requests_you've_received.json file
                with open(os.path.join(root_dir, "connections", "followers_and_following", "follow_requests_you've_received.json"), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the data has a 'structure' key
                    if 'structure' in data:
                        # Iterate over the relationships_follow_requests_received list
                        for item in data.get('structure', {}).get('relationships_follow_requests_received', []):
                            # Extract the title (profile name)
                            profile = item.get('title')
                            # Iterate over the relationships_following list
                            for item in data.get('structure', {}).get('relationships_following', []):
                                # Check if the profile is in the list
                                if profile in [item.get('title') for item in item.get('string_list_data', [])]:
                                    # If the profile is in the list, skip it
                                    continue
                                # If the profile is not in the list, add it to the profiles list
                                profiles.append(profile)

# Write the profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([(profile,) for profile in profiles])