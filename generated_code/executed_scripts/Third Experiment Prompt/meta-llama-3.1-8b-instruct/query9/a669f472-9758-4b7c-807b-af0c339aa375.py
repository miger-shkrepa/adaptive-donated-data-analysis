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
for connection in os.listdir(os.path.join(root_dir, "connections")):
    # Check if the connection is a directory
    if os.path.isdir(os.path.join(root_dir, "connections", connection)):
        # Iterate over the followers and following directory
        for following in os.listdir(os.path.join(root_dir, "connections", connection)):
            # Check if the following is a JSON file
            if following.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, "connections", connection, following), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the data has a structure
                    if "structure" in data:
                        # Iterate over the relationships
                        for relationship in data["structure"]:
                            # Check if the relationship has a title
                            if "title" in relationship:
                                # Check if the title is "following"
                                if relationship["title"] == "following":
                                    # Iterate over the followers
                                    for follower in relationship["string_list_data"]:
                                        # Check if the follower has a value
                                        if "value" in follower:
                                            # Check if the value is the user's profile
                                            if follower["value"] == "user_profile":
                                                # Iterate over the relationships
                                                for relationship in data["structure"]:
                                                    # Check if the relationship has a title
                                                    if "title" in relationship:
                                                        # Check if the title is "followers"
                                                        if relationship["title"] == "followers":
                                                            # Iterate over the followers
                                                            for follower in relationship["string_list_data"]:
                                                                # Check if the follower has a value
                                                                if "value" in follower:
                                                                    # Check if the value is not the user's profile
                                                                    if follower["value"] != "user_profile":
                                                                        # Add the profile to the list
                                                                        profiles.append(follower["value"])

# Write the profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([profile for profile in profiles])