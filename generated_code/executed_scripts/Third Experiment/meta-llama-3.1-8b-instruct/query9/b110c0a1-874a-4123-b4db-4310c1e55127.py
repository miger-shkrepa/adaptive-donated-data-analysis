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
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)
            
            # Check if the JSON file contains the required structure
            if "relationships_follow_requests_received" in data:
                # Iterate over the relationships
                for relationship in data["relationships_follow_requests_received"]:
                    # Check if the relationship has a title
                    if "title" in relationship:
                        # Add the title to the profiles list
                        profiles.append(relationship["title"])
            
            # Check if the JSON file contains the required structure
            if "relationships_follow_requests_sent" in data:
                # Iterate over the relationships
                for relationship in data["relationships_follow_requests_sent"]:
                    # Check if the relationship has a title
                    if "title" in relationship:
                        # Add the title to the profiles list
                        profiles.append(relationship["title"])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    for profile in profiles:
        writer.writerow([profile])