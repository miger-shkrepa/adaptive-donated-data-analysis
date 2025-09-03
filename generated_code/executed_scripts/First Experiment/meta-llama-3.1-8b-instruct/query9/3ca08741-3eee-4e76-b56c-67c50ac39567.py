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
            
            # Check if the JSON file contains the required information
            if 'followers_and_following' in data and 'following.json' in data['followers_and_following']:
                # Open the following.json file
                with open(os.path.join(root_dir, 'followers_and_following', 'following.json'), 'r') as following_file:
                    # Load the following.json data
                    following_data = json.load(following_file)
                    
                    # Check if the following.json file contains the required information
                    if 'relationships_following' in following_data:
                        # Iterate over the relationships in the following.json file
                        for relationship in following_data['relationships_following']:
                            # Check if the relationship contains the required information
                            if 'string_list_data' in relationship and relationship['string_list_data']:
                                # Iterate over the strings in the relationship
                                for string in relationship['string_list_data']:
                                    # Check if the string contains the required information
                                    if 'href' in string and 'timestamp' in string and 'value' in string:
                                        # Extract the profile information from the string
                                        profile = string['value']
                                        
                                        # Check if the profile is in the profiles list
                                        if profile not in profiles:
                                            # Add the profile to the profiles list
                                            profiles.append(profile)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(['Profile'])
    
    # Write the profiles to the CSV file
    for profile in profiles:
        writer.writerow([profile])