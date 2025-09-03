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

# Iterate over the 'connections' directory
for dir in os.listdir(os.path.join(root_dir, "connections")):
    if dir == "followers_and_following":
        # Iterate over the 'followers_and_following' directory
        for file in os.listdir(os.path.join(root_dir, "connections", dir)):
            if file == "following.json":
                # Open the 'following.json' file
                try:
                    with open(os.path.join(root_dir, "connections", dir, file), 'r') as f:
                        # Load the JSON data
                        data = json.load(f)
                        # Check if the 'structure' key exists
                        if 'structure' in data:
                            # Extract the 'relationships_following' list
                            following = data['structure']['relationships_following']
                            # Iterate over the 'relationships_following' list
                            for item in following:
                                # Extract the 'string_list_data' list
                                string_list_data = item.get('string_list_data', [])
                                # Iterate over the 'string_list_data' list
                                for profile in string_list_data:
                                    # Check if the profile is not in the 'close_friends.json' file
                                    if not os.path.exists(os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json")):
                                        # If the file does not exist, treat its contribution as 0
                                        continue
                                    with open(os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json"), 'r') as f:
                                        # Load the JSON data
                                        data = json.load(f)
                                        # Check if the 'structure' key exists
                                        if 'structure' in data:
                                            # Extract the 'relationships_close_friends' list
                                            close_friends = data['structure']['relationships_close_friends']
                                            # Iterate over the 'relationships_close_friends' list
                                            for close_friend in close_friends:
                                                # Extract the 'string_list_data' list
                                                string_list_data = close_friend.get('string_list_data', [])
                                                # Iterate over the 'string_list_data' list
                                                for close_friend_profile in string_list_data:
                                                    # Check if the close friend profile is the same as the profile
                                                    if close_friend_profile.get('value') == profile.get('value'):
                                                        # If the profiles are the same, skip this iteration
                                                        continue
                                            # If the profile is not in the 'close_friends.json' file, add it to the list
                                            profiles.append(profile.get('value', ''))
                except json.JSONDecodeError:
                    # If the JSON file is invalid, skip it
                    pass

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([(profile,) for profile in profiles])