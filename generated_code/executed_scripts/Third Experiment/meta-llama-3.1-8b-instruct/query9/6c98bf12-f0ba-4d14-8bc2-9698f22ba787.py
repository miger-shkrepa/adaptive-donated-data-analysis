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
            data = file.read()
            # Check if the JSON data contains the necessary information
            if "relationships_follow_requests_sent" in data:
                # Extract the profiles from the JSON data
                profiles.extend([profile["title"] for profile in data["relationships_follow_requests_sent"]])
            elif "relationships_follow_requests_received" in data:
                # Extract the profiles from the JSON data
                profiles.extend([profile["title"] for profile in data["relationships_follow_requests_received"]])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    for profile in profiles:
        writer.writerow([profile])