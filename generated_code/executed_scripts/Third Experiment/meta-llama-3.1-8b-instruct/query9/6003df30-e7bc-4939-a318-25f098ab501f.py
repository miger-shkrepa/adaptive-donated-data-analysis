import csv
import os

# Declare the variable referring to the file input
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

            # Check if the JSON file contains the required data
            if "following.json" in data and "relationships_following" in data["following.json"]["structure"]:
                # Iterate over the relationships
                for relationship in data["following.json"]["structure"]["relationships_following"]:
                    # Check if the relationship contains the required data
                    if "string_list_data" in relationship and "href" in relationship["string_list_data"][0] and "timestamp" in relationship["string_list_data"][0] and "value" in relationship["string_list_data"][0]:
                        # Check if the user is not followed back
                        if "follow_requests_you've_received.json" in data and "relationships_follow_requests_received" in data["follow_requests_you've_received.json"]["structure"]:
                            for request in data["follow_requests_you've_received.json"]["structure"]["relationships_follow_requests_received"]:
                                if "string_list_data" in request and "href" in request["string_list_data"][0] and "timestamp" in request["string_list_data"][0] and "value" in request["string_list_data"][0]:
                                    if relationship["string_list_data"][0]["href"] == request["string_list_data"][0]["href"]:
                                        break
                            else:
                                # Add the profile to the list
                                profiles.append(relationship["title"])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    writer.writerows([[profile] for profile in profiles])  # Write the profiles