import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of profiles that the user follows but are not followed back
followed_profiles = []

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections")):
    for filename in filenames:
        if filename.startswith("following"):
            # Open the file and read its contents
            file_path = os.path.join(dirpath, filename)
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = f.read()
                    # Parse the JSON data
                    data = json.loads(data)
                    # Extract the relationships_following list
                    relationships_following = data.get("structure", {}).get("relationships_following", [])
                    # Iterate over the relationships_following list
                    for relationship in relationships_following:
                        # Extract the title of the relationship
                        title = relationship.get("title", "")
                        # Check if the title is a profile
                        if title.startswith("profile_"):
                            # Extract the profile ID
                            profile_id = title.split("_")[1]
                            # Check if the profile is not followed back
                            unfollowed_profiles = [relationship["title"] for relationship in data.get("structure", {}).get("relationships_unfollowed_users", [])]
                            if profile_id not in unfollowed_profiles:
                                # Add the profile to the followed_profiles list
                                followed_profiles.append(profile_id)

# Write the followed_profiles list to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in followed_profiles])