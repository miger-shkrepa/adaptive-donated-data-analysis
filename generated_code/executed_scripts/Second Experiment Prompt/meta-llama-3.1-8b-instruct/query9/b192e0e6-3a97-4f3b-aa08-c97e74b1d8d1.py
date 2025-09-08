import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of profiles that the user follows but are not followed back
profiles_followed_back = []

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the followers and following directory
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
                                # Extract the profile ID
                                profile_id = item.get('string_list_data', [{}])[0].get('value', '')
                                # Check if the profile follows the user back
                                following_back = False
                                for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
                                    if "followers_1.json" in filenames:
                                        try:
                                            with open(os.path.join(dirpath, "followers_1.json"), "r") as f:
                                                data = json.load(f)
                                                for item in data['structure'].get('relationships_following', []):
                                                    if item.get('string_list_data', [{}])[0].get('value', '') == profile_id:
                                                        following_back = True
                                                        break
                                        except FileNotFoundError:
                                            # If the followers_1.json file does not exist, treat its contribution as 0
                                            pass
                                # If the profile does not follow the user back, add it to the list
                                if not following_back:
                                    profiles_followed_back.append(profile_id)
                except FileNotFoundError:
                    # If the following.json file does not exist, treat its contribution as 0
                    pass

# Write the list of profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows(profiles_followed_back)