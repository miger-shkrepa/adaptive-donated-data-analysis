import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of profiles that the user follows but do not follow back
profiles_followed_back = []

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the followers_and_following directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
            # Check if the close_friends.json file exists
            if "close_friends.json" in filenames:
                # Open the close_friends.json file
                with open(os.path.join(dirpath, "close_friends.json"), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Iterate over the relationships_close_friends list
                    for item in data["relationships_close_friends"]:
                        # Check if the string_list_data list is not empty
                        if item["string_list_data"]:
                            # Iterate over the string_list_data list
                            for item in item["string_list_data"]:
                                # Check if the value is not None
                                if item["value"]:
                                    # Add the profile to the list of profiles that the user follows but do not follow back
                                    profiles_followed_back.append(item["value"])

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the followers_and_following directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
            # Check if the following.json file exists
            if "following.json" in filenames:
                # Open the following.json file
                with open(os.path.join(dirpath, "following.json"), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Iterate over the relationships_following list
                    for item in data["relationships_following"]:
                        # Check if the string_list_data list is not empty
                        if item["string_list_data"]:
                            # Iterate over the string_list_data list
                            for item in item["string_list_data"]:
                                # Check if the value is not None
                                if item["value"]:
                                    # Check if the profile is in the list of profiles that the user follows but do not follow back
                                    if item["value"] in profiles_followed_back:
                                        # Remove the profile from the list of profiles that the user follows but do not follow back
                                        profiles_followed_back.remove(item["value"])

# Write the list of profiles that the user follows but do not follow back to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([profile for profile in profiles_followed_back])