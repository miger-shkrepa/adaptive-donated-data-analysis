import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the JSON files in the directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the 'following' data
            if 'following.json' in data:
                # Iterate over the profiles in the 'following' data
                for profile in data['following.json']['structure']['relationships_following']:
                    # Check if the profile has a 'string_list_data' key
                    if 'string_list_data' in profile:
                        # Iterate over the strings in the 'string_list_data'
                        for string in profile['string_list_data']:
                            # Check if the string has a 'value' key
                            if 'value' in string:
                                # Check if the value is not empty
                                if string['value']:
                                    # Add the profile to the list
                                    profiles.append(profile['title'])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    for profile in profiles:
        writer.writerow([profile])

print("Query completed successfully.")