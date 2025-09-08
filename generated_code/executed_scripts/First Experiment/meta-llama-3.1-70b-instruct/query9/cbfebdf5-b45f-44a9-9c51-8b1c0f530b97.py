import os
import json
import csv

root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize an empty set to store the followers
    followers = set()

    # Initialize an empty set to store the following
    following = set()

    # Iterate over the subdirectories in the root directory
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)

        # Check if the subdirectory is 'followers_and_following'
        if subdir == 'followers_and_following':
            # Iterate over the files in the 'followers_and_following' subdirectory
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)

                # Check if the file is 'followers_1.json'
                if filename == 'followers_1.json':
                    # Open the 'followers_1.json' file and load the data
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    # Iterate over the followers and add them to the set
                    for follower in data:
                        followers.add(follower['title'])

                # Check if the file is 'following.json'
                elif filename == 'following.json':
                    # Open the 'following.json' file and load the data
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    # Iterate over the following and add them to the set
                    for follow in data['relationships_following']:
                        following.add(follow['title'])

    # Find the profiles that the user follows but do not follow him back
    not_following_back = following - followers

    # Create a CSV file and write the results
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in not_following_back:
            writer.writerow([profile])

except FileNotFoundError as e:
    raise FileNotFoundError(f"FileNotFoundError: {e}")

except json.JSONDecodeError as e:
    raise ValueError(f"ValueError: Error parsing JSON - {e}")

except Exception as e:
    raise ValueError(f"ValueError: An error occurred - {e}")