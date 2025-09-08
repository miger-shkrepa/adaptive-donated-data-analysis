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
            if 'following.json' in data:
                # Extract the relationships_following data
                relationships_following = data['following.json']['structure']['relationships_following']

                # Iterate over the relationships_following data
                for relationship in relationships_following:
                    # Check if the relationship has a string_list_data
                    if 'string_list_data' in relationship:
                        # Extract the string_list_data
                        string_list_data = relationship['string_list_data']

                        # Check if the string_list_data contains the user's profile
                        if any(item['value'] == 'user' for item in string_list_data):
                            # Extract the profiles that the user follows
                            profiles.extend([item['value'] for item in string_list_data if item['value'] != 'user'])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Profile'])  # Write the column headers
    writer.writerows([(profile,) for profile in profiles])  # Write the profiles

print("The script has finished executing.")