import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the connections directory
for dir in os.listdir(os.path.join(root_dir, "connections")):
    if dir == "followers_and_following":
        # Initialize an empty list to store the followers
        followers = []
        
        # Initialize an empty list to store the following
        following = []
        
        # Iterate over the followers and following directory
        for file in os.listdir(os.path.join(root_dir, "connections", "followers_and_following")):
            if file == "followers_1.json":
                # Try to open the followers_1.json file
                try:
                    with open(os.path.join(root_dir, "connections", "followers_and_following", file), "r") as f:
                        data = json.load(f)
                        # Iterate over the relationships_followers list
                        for relationship in data:
                            # Extract the title (profile name)
                            follower = relationship["title"]
                            # Add the follower to the list
                            followers.append(follower)
                except FileNotFoundError:
                    # If the file does not exist, treat its contribution as 0
                    pass
            
            elif file == "following.json":
                # Try to open the following.json file
                try:
                    with open(os.path.join(root_dir, "connections", "followers_and_following", file), "r") as f:
                        data = json.load(f)
                        # Check if the 'structure' key exists
                        if 'structure' in data:
                            # Iterate over the relationships_following list
                            for relationship in data["structure"]["relationships_following"]:
                                # Extract the title (profile name)
                                profile = relationship["title"]
                                # Add the profile to the list
                                following.append(profile)
                        else:
                            # If the 'structure' key does not exist, treat its contribution as 0
                            pass
                except FileNotFoundError:
                    # If the file does not exist, treat its contribution as 0
                    pass
        
        # Iterate over the following list
        for profile in following:
            # Check if the profile is not in the followers list
            if profile not in followers:
                # Add the profile to the list
                profiles.append(profile)

# Write the profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([(profile,) for profile in profiles])