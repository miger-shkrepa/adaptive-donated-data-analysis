import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of profiles that the user follows but are not followed back
profiles_followed_back = []

# Iterate over the connections directory
for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "connections", "followers_and_following")):
    # Check if the directory contains the 'following.json' file
    if 'following.json' in filenames:
        # Open the 'following.json' file
        with open(os.path.join(dirpath, 'following.json'), 'r') as f:
            # Load the JSON data
            data = json.load(f)
            # Check if the data has a 'structure' key
            if 'structure' in data:
                # Iterate over the relationships_following list
                for item in data['structure'].get('relationships_following', []):
                    # Check if the item has a string_list_data with a timestamp and a value
                    if 'string_list_data' in item and any(isinstance(x, dict) and 'timestamp' in x and 'value' in x for x in item['string_list_data']):
                        # Extract the timestamp and value from the string_list_data
                        timestamp = [x['timestamp'] for x in item['string_list_data'] if isinstance(x, dict) and 'timestamp' in x][0]
                        value = [x['value'] for x in item['string_list_data'] if isinstance(x, dict) and 'value' in x][0]
                        # Check if the value is a profile ID
                        if value.isdigit():
                            # Check if the profile ID is in the 'close_friends.json' file
                            close_friends_path = os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json")
                            if os.path.exists(close_friends_path):
                                with open(close_friends_path, 'r') as close_friends_f:
                                    close_friends_data = json.load(close_friends_f)
                                    # Check if the close_friends_data has a 'structure' key
                                    if 'structure' in close_friends_data:
                                        # Iterate over the relationships_close_friends list
                                        for close_friend in close_friends_data['structure'].get('relationships_close_friends', []):
                                            # Check if the item has a string_list_data with a timestamp and a value
                                            if 'string_list_data' in close_friend and any(isinstance(x, dict) and 'timestamp' in x and 'value' in x for x in close_friend['string_list_data']):
                                                close_friend_timestamp = [x['timestamp'] for x in close_friend['string_list_data'] if isinstance(x, dict) and 'timestamp' in x][0]
                                                close_friend_value = [x['value'] for x in close_friend['string_list_data'] if isinstance(x, dict) and 'value' in x][0]
                                                if close_friend_value == value and close_friend_timestamp > timestamp:
                                                    # If the profile is in the 'close_friends.json' file and the timestamp is greater than the timestamp of the profile in the 'following.json' file, add it to the list of profiles that the user follows but are not followed back
                                                    profiles_followed_back.append(value)

# Write the list of profiles that the user follows but are not followed back to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles_followed_back])