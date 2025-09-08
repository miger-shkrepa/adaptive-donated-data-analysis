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
                # Load the JSON file
                with open(os.path.join(root_dir, "connections", connection, following), "r") as f:
                    data = json.load(f)
                # Check if the JSON file has the correct structure
                if "type" in data and data["type"] == "json":
                    # Iterate over the following profiles
                    for profile in data["structure"]["relationships_following"]:
                        # Check if the profile is not following the user back
                        if "string_list_data" in profile and "href" in profile["string_list_data"][0] and profile["string_list_data"][0]["href"] != "self":
                            # Add the profile to the list
                            profiles.append(profile["title"])

# Write the profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])