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
for connection in os.listdir(os.path.join(root_dir, "connections")):
    # Check if the connection is a directory
    if os.path.isdir(os.path.join(root_dir, "connections", connection)):
        # Iterate over the followers and following directory
        for follower in os.listdir(os.path.join(root_dir, "connections", connection)):
            # Check if the follower is a JSON file
            if follower.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, "connections", connection, follower), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the JSON data has a structure
                    if "structure" in data:
                        # Iterate over the relationships
                        for relationship in data["structure"]:
                            # Check if the relationship is a follower
                            if relationship["title"] == "followers":
                                # Iterate over the followers
                                for follower in relationship["string_list_data"]:
                                    # Check if the follower is not the user
                                    if follower["value"] != "self":
                                        # Check if the follower is not following the user back
                                        if not any(following["value"] == follower["value"] for following in relationship["string_list_data"]):
                                            # Add the follower to the list of profiles that the user follows but do not follow back
                                            profiles_followed_back.append(follower["value"])

# Write the list of profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows(profiles_followed_back)