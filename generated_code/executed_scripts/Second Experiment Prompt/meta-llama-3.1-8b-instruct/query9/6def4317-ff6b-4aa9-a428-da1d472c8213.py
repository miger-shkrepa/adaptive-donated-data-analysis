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
for item in os.listdir(os.path.join(root_dir, "connections")):
    # Check if the item is a directory
    if os.path.isdir(os.path.join(root_dir, "connections", item)):
        # Iterate over the followers_and_following directory
        for subitem in os.listdir(os.path.join(root_dir, "connections", item)):
            # Check if the subitem is a directory
            if os.path.isdir(os.path.join(root_dir, "connections", item, subitem)):
                # Iterate over the JSON files in the subdirectory
                for filename in os.listdir(os.path.join(root_dir, "connections", item, subitem)):
                    # Check if the file is a JSON file
                    if filename.endswith(".json"):
                        # Open the JSON file
                        with open(os.path.join(root_dir, "connections", item, subitem, filename), "r") as f:
                            # Load the JSON data
                            data = json.load(f)
                            # Check if the data has a structure
                            if "structure" in data:
                                # Iterate over the structure
                                for item in data["structure"]:
                                    # Check if the item is a list
                                    if isinstance(item, list):
                                        # Iterate over the list
                                        for subitem in item:
                                            # Check if the subitem is a dictionary
                                            if isinstance(subitem, dict):
                                                # Check if the dictionary has a "string_list_data" key
                                                if "string_list_data" in subitem:
                                                    # Iterate over the "string_list_data" list
                                                    for profile in subitem["string_list_data"]:
                                                        # Check if the profile has a "href" key
                                                        if "href" in profile:
                                                            # Add the profile to the list
                                                            profiles.append(profile["href"])

# Write the profiles to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([(profile,) for profile in profiles])