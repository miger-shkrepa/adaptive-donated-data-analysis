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
            if "following.json" in filenames:
                # Open the following.json file
                try:
                    with open(os.path.join(dirpath, "following.json"), "r") as f:
                        data = json.load(f)
                        # Check if the data has a 'structure' key
                        if 'structure' in data:
                            # Iterate over the relationships_following list
                            for item in data['structure'].get('relationships_following', []):
                                # Extract the profile name
                                profile = item.get('string_list_data', [{}])[0].get('value')
                                # Check if the profile is not in the close_friends.json file
                                close_friends_path = os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json")
                                if not os.path.exists(close_friends_path):
                                    # If the file does not exist, treat its contribution as 0
                                    profiles.append(profile)
                                else:
                                    try:
                                        with open(close_friends_path, "r") as close_friends_f:
                                            close_friends_data = json.load(close_friends_f)
                                            # Check if the close_friends_data has a 'structure' key
                                            if 'structure' in close_friends_data:
                                                # Iterate over the relationships_close_friends list
                                                for close_friend in close_friends_data['structure'].get('relationships_close_friends', []):
                                                    # Check if the profile is in the close_friends list
                                                    if profile in close_friend.get('string_list_data', [{}])[0].get('value'):
                                                        # If the profile is in the close_friends list, skip it
                                                        break
                                                else:
                                                    # If the profile is not in the close_friends list, add it to the profiles list
                                                    profiles.append(profile)
                                    except json.JSONDecodeError:
                                        # If the close_friends.json file is not a valid JSON, treat its contribution as 0
                                        profiles.append(profile)
                except json.JSONDecodeError:
                    # If the following.json file is not a valid JSON, treat its contribution as 0
                    pass

# Write the profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([(profile,) for profile in profiles])