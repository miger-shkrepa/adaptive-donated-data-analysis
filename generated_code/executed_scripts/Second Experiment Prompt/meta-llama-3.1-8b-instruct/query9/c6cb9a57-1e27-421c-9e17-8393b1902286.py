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

# Initialize an empty set to store the profiles that follow the user back
following_back = set()

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the followers_and_following directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
            if "following.json" in filenames:
                # Open the following.json file
                with open(os.path.join(dirpath, "following.json"), "r") as f:
                    data = json.load(f)
                    # Check if the data has a 'structure' key
                    if 'structure' in data:
                        # Extract the relationships_following list
                        following = data["structure"]["relationships_following"]
                        # Iterate over the relationships_following list
                        for item in following:
                            # Extract the string_list_data list
                            string_list_data = item.get("string_list_data", [])
                            # Iterate over the string_list_data list
                            for item in string_list_data:
                                # Extract the value
                                value = item.get("value", "")
                                # Check if the value is a valid profile ID
                                if value.isdigit():
                                    # Add the profile to the profiles list
                                    profiles.append(value)

            if "followers_1.json" in filenames:
                # Open the followers_1.json file
                with open(os.path.join(dirpath, "followers_1.json"), "r") as f:
                    data = json.load(f)
                    # Check if the data has a 'structure' key
                    if 'structure' in data:
                        # Extract the relationships_followers list
                        followers = data["structure"]["relationships_followers"]
                        # Iterate over the relationships_followers list
                        for item in followers:
                            # Extract the string_list_data list
                            string_list_data = item.get("string_list_data", [])
                            # Iterate over the string_list_data list
                            for item in string_list_data:
                                # Extract the value
                                value = item.get("value", "")
                                # Check if the value is a valid profile ID
                                if value.isdigit():
                                    # Add the profile to the profiles list
                                    profiles.append(value)
                                    # Add the profile to the following_back set
                                    following_back.add(value)

# Write the profiles that do not follow the user back to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    for profile in profiles:
        if profile not in following_back:
            writer.writerow([profile])