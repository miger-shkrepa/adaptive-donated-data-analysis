import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'impressions_history_posts_seen' in data and 'story_activities_story_likes' in data:
                # Iterate over the posts viewed by the user
                for post in data['impressions_history_posts_seen']:
                    # Check if the post has a string map data
                    if 'string_map_data' in post:
                        # Iterate over the string map data
                        for key, value in post['string_map_data'].items():
                            # Check if the key is 'Author'
                            if key == 'Author':
                                # Add the author to the list of accounts
                                accounts.append(value['value'])

                # Iterate over the story likes
                for story in data['story_activities_story_likes']:
                    # Check if the story has a string list data
                    if 'string_list_data' in story:
                        # Iterate over the string list data
                        for timestamp in story['string_list_data']:
                            # Check if the timestamp is an integer
                            if isinstance(timestamp, int):
                                # Add the account to the list of accounts
                                accounts.append('')

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Account'])  # Write the header
    writer.writerows([[account] for account in accounts])  # Write the accounts