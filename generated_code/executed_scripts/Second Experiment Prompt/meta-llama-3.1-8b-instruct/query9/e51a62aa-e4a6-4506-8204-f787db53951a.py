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

# Iterate over the 'connections' directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the 'followers_and_following' directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
            if "following.json" in filenames:
                # Open the 'following.json' file
                with open(os.path.join(dirpath, "following.json"), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the 'structure' key exists
                    if 'structure' in data:
                        # Iterate over the 'relationships_following' list
                        for item in data['structure']['relationships_following']:
                            # Extract the 'string_list_data' list
                            string_list_data = item.get('string_list_data', [])
                            # Iterate over the 'string_list_data' list
                            for item in string_list_data:
                                # Extract the 'value' field
                                value = item.get('value', '')
                                # Check if the value is a valid profile ID
                                if value.isdigit():
                                    # Add the profile ID to the list of profiles that the user follows
                                    profiles_followed_back.append(value)

# Iterate over the 'connections' directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    if "followers_and_following" in dirnames:
        # Iterate over the 'followers_and_following' directory
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
            if "followers_1.json" in filenames:
                # Open the 'followers_1.json' file
                with open(os.path.join(dirpath, "followers_1.json"), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the 'structure' key exists
                    if 'structure' in data:
                        # Iterate over the 'string_list_data' list
                        for item in data['structure'].get('string_list_data', []):
                            # Extract the 'value' field
                            value = item.get('value', '')
                            # Check if the value is a valid profile ID
                            if value.isdigit():
                                # Add the profile ID to the list of profiles that follow the user
                                profiles_followed_back = [profile for profile in profiles_followed_back if profile != value]

# Write the list of profiles that the user follows but are not followed back to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([profile for profile in profiles_followed_back if profile is not None])