import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the necessary data
            if "follow_requests_you've_received.json" in data and "recently_unfollowed_profiles.json" in data:
                # Extract the follow requests and recently unfollowed profiles
                follow_requests = data["follow_requests_you've_received.json"]["structure"]["relationships_follow_requests_received"]
                recently_unfollowed_profiles = data["recently_unfollowed_profiles.json"]["structure"]["relationships_unfollowed_users"]

                # Iterate over the follow requests
                for follow_request in follow_requests:
                    # Iterate over the recently unfollowed profiles
                    for recently_unfollowed_profile in recently_unfollowed_profiles:
                        # Check if the follow request is not in the recently unfollowed profiles
                        if follow_request["title"] not in [profile["title"] for profile in recently_unfollowed_profile["string_list_data"]]:
                            # Add the profile to the list
                            profiles.append(follow_request["title"])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    for profile in profiles:
        writer.writerow([profile])