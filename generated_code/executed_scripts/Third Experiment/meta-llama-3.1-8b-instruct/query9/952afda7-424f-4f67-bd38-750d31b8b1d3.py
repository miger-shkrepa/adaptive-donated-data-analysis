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

            # Check if the JSON file contains the required data
            if 'connections' in data and 'followers_and_following' in data['connections'] and 'following.json' in data['connections']['followers_and_following']:
                # Load the following data
                following_data = data['connections']['followers_and_following']['following.json']

                # Check if the following data contains the required structure
                if 'relationships_following' in following_data['structure']:
                    # Iterate over the following data
                    for following in following_data['structure']['relationships_following']:
                        # Check if the following data contains the required structure
                        if 'string_list_data' in following and 'href' in following['string_list_data'][0] and 'timestamp' in following['string_list_data'][0] and 'value' in following['string_list_data'][0]:
                            # Iterate over the string list data
                            for item in following['string_list_data']:
                                # Check if the item contains the required structure
                                if 'href' in item and 'timestamp' in item and 'value' in item:
                                    # Add the profile to the list
                                    profiles.append(item['value'])

            # Check if the JSON file contains the required data
            if 'connections' in data and 'followers_and_following' in data['connections'] and 'followers_1.json' in data['connections']['followers_and_following']:
                # Load the followers data
                followers_data = data['connections']['followers_and_following']['followers_1.json']

                # Check if the followers data contains the required structure
                if 'relationships_follow_requests_received' in followers_data['structure']:
                    # Iterate over the followers data
                    for followers in followers_data['structure']['relationships_follow_requests_received']:
                        # Check if the followers data contains the required structure
                        if 'string_list_data' in followers and 'href' in followers['string_list_data'][0] and 'timestamp' in followers['string_list_data'][0] and 'value' in followers['string_list_data'][0]:
                            # Iterate over the string list data
                            for item in followers['string_list_data']:
                                # Check if the item contains the required structure
                                if 'href' in item and 'timestamp' in item and 'value' in item:
                                    # Check if the profile is in the following data
                                    if item['value'] not in [profile['value'] for profile in profiles]:
                                        # Add the profile to the list
                                        profiles.append(item['value'])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Profile'])
    writer.writerows([(profile,) for profile in profiles])