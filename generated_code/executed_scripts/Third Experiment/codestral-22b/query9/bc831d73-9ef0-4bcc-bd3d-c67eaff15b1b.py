import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Navigate to the relationships_permanent_follow_requests directory
relationships_dir = os.path.join(root_dir, "relationships_permanent_follow_requests")

# Check if the relationships directory exists
if os.path.exists(relationships_dir):
    # Iterate over the JSON files in the directory
    for filename in os.listdir(relationships_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(relationships_dir, filename)
            # Open the JSON file
            with open(filepath, "r") as f:
                data = json.load(f)
                # Extract the profiles that the user follows
                followed_profiles = [item["value"] for item in data["string_list_data"]]
                # Add the profiles to the list
                profiles.extend(followed_profiles)

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])