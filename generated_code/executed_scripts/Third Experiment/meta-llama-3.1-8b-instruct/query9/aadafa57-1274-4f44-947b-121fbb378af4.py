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

            # Check if the JSON file contains the 'following' data
            if 'following' in data:
                # Iterate over the profiles in the 'following' data
                for profile in data['following']:
                    # Check if the profile has a 'title' key
                    if 'title' in profile:
                        # Add the profile to the list
                        profiles.append(profile['title'])

# Initialize an empty list to store the profiles that do not follow back
profiles_not_following_back = []

# Iterate over the profiles
for profile in profiles:
    # Check if the profile exists in the 'following' data
    if profile in [p['title'] for p in data['following']]:
        # Add the profile to the list
        profiles_not_following_back.append(profile)

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Profile'])  # Write the column headers
    writer.writerows([(profile,) for profile in profiles_not_following_back])  # Write the profiles