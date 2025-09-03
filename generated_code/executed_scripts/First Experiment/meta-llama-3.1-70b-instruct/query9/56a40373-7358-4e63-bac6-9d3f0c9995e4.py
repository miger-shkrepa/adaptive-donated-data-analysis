import os
import json
import csv

root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize an empty set to store the profiles the user follows
    following_profiles = set()

    # Initialize an empty set to store the profiles that follow the user
    follower_profiles = set()

    # Iterate over the subdirectories in the root directory
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)

        # Check if the subdirectory is 'followers_and_following'
        if subdir == 'followers_and_following':
            # Iterate over the files in the 'followers_and_following' subdirectory
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)

                # Check if the file is 'following.json'
                if filename == 'following.json':
                    # Open and load the 'following.json' file
                    with open(file_path, 'r') as file:
                        following_data = json.load(file)

                    # Extract the profiles the user follows
                    for profile in following_data['relationships_following']:
                        following_profiles.add(profile['title'])

                # Check if the file is 'followers_1.json'
                elif filename == 'followers_1.json':
                    # Open and load the 'followers_1.json' file
                    with open(file_path, 'r') as file:
                        follower_data = json.load(file)

                    # Extract the profiles that follow the user
                    for profile in follower_data:
                        follower_profiles.add(profile['title'])

    # Calculate the profiles the user follows that do not follow him back
    non_reciprocal_following = following_profiles - follower_profiles

    # Save the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in non_reciprocal_following:
            writer.writerow([profile])

except FileNotFoundError as e:
    raise FileNotFoundError(f"FileNotFoundError: {e}")
except json.JSONDecodeError as e:
    raise ValueError(f"ValueError: Error parsing JSON - {e}")
except Exception as e:
    raise ValueError(f"ValueError: An error occurred - {e}")