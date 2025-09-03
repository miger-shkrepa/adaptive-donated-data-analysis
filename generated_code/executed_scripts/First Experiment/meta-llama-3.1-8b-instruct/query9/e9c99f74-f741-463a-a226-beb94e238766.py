import os
import csv
import json

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
            data = json.load(file)
            
            # Check if the JSON data contains the required information
            if 'following' in data and 'relationships_following' in data['following']:
                # Iterate over the relationships
                for relationship in data['following']['relationships_following']:
                    # Check if the relationship contains the required information
                    if 'string_list_data' in relationship and 'href' in relationship['string_list_data'][0]:
                        # Extract the profile information
                        profile = relationship['string_list_data'][0]['href']
                        
                        # Check if the profile is in the profiles list
                        if profile not in profiles:
                            # Add the profile to the profiles list
                            profiles.append(profile)

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    for profile in profiles:
        writer.writerow([profile])