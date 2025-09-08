import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the JSON files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Check if the JSON data contains the required information
            if "following.json" in data:
                # Parse the JSON data
                import json
                json_data = json.loads(data)
                # Extract the relationships_following information
                relationships_following = json_data["following.json"]["structure"]["relationships_following"]
                # Extract the relationships_follow_requests_received information
                relationships_follow_requests_received = json_data["follow_requests_you've_received.json"]["structure"]["relationships_follow_requests_received"]
                # Iterate over the relationships_following information
                for relationship in relationships_following:
                    # Iterate over the relationships_follow_requests_received information
                    for received_relationship in relationships_follow_requests_received:
                        # Check if the profile is not following back
                        if relationship["title"] != received_relationship["title"]:
                            # Add the profile to the list
                            profiles.append(relationship["title"])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Profile"])
    # Write the profiles
    for profile in profiles:
        writer.writerow([profile])