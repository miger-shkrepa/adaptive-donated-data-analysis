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

# Iterate over the 'connections' directory
for dir in os.listdir(os.path.join(root_dir, "connections")):
    if dir == "followers_and_following":
        # Iterate over the 'followers_and_following' directory
        for file in os.listdir(os.path.join(root_dir, "connections", "followers_and_following")):
            if file == "following.json":
                # Open the 'following.json' file
                try:
                    with open(os.path.join(root_dir, "connections", "followers_and_following", file), 'r') as f:
                        # Load the JSON data
                        data = json.load(f)
                        # Check if the 'structure' key exists in the data
                        if 'structure' in data:
                            # Iterate over the 'relationships_following' list
                            for item in data.get('structure', {}).get('relationships_following', []):
                                # Get the 'string_list_data' list
                                followers = item.get('string_list_data', [])
                                # Iterate over the followers
                                for follower in followers:
                                    # Get the 'href' value
                                    href = follower.get('href')
                                    # Check if the follower is in the 'close_friends.json' file
                                    close_friends_file = os.path.join(root_dir, "connections", "followers_and_following", "close_friends.json")
                                    if os.path.exists(close_friends_file):
                                        with open(close_friends_file, 'r') as close_friends_f:
                                            close_friends_data = json.load(close_friends_f)
                                            # Check if the 'structure' key exists in the close_friends_data
                                            if 'structure' in close_friends_data:
                                                # Iterate over the 'relationships_close_friends' list
                                                for close_friend in close_friends_data['structure']['relationships_close_friends']:
                                                    # Get the 'string_list_data' list
                                                    close_friends = close_friend.get('string_list_data', [])
                                                    # Check if the follower is in the 'close_friends' list
                                                    if href in [f.get('href') for f in close_friends]:
                                                        # If the follower is in the 'close_friends' list, skip this iteration
                                                        continue
                                    # If the follower is not in the 'close_friends' list, add the profile to the list
                                    profiles_followed_back.append(href)
                except FileNotFoundError:
                    # If the 'close_friends.json' file does not exist, treat its contribution as 0 and continue processing the rest
                    pass

# Write the list of profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])
    writer.writerows([[p] for p in profiles_followed_back])