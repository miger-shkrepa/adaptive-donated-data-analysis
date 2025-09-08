import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the JSON files in the 'followers_and_following' directory
for file in os.listdir(root_dir):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, file), 'r') as f:
            # Load the JSON data
            data = eval(f.read())

            # Check if the file contains the necessary data
            if 'followers_1.json' in data and 'following.json' in data:
                # Extract the followers and following data
                followers = data['followers_1.json']['structure']
                following = data['following.json']['structure']

                # Iterate over the followers
                for follower in followers:
                    # Check if the follower is in the following list
                    if any(following_item['title'] == follower['title'] for following_item in following):
                        # If the follower is in the following list, skip this follower
                        continue

                    # Add the follower to the profiles list
                    profiles.append(follower['title'])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    writer.writerows([[profile] for profile in profiles])  # Write the profiles