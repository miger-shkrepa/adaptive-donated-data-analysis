import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
accounts = []
post_views = []
video_views = []

# Iterate over the media directory
for media_dir in os.listdir(root_dir):
    # Check if the media directory is a file
    if os.path.isfile(os.path.join(root_dir, media_dir)):
        # Check if the file is a JSON file
        if media_dir.endswith('.json'):
            # Open the JSON file
            with open(os.path.join(root_dir, media_dir), 'r') as file:
                # Read the JSON file
                data = file.read()
                # Check if the JSON file contains the required data
                if 'profile_user' in data:
                    # Extract the account name
                    account = media_dir.split('.')[0]
                    # Extract the post views and video views
                    post_views.append(0)
                    video_views.append(0)
                    accounts.append(account)
                elif 'profile_business' in data:
                    # Extract the account name
                    account = media_dir.split('.')[0]
                    # Extract the post views and video views
                    post_views.append(0)
                    video_views.append(0)
                    accounts.append(account)
                elif 'profile_profile_change' in data:
                    # Extract the account name
                    account = media_dir.split('.')[0]
                    # Extract the post views and video views
                    post_views.append(0)
                    video_views.append(0)
                    accounts.append(account)
    # Iterate over the media directory
    elif os.path.isdir(os.path.join(root_dir, media_dir)):
        # Check if the media directory is a file
        if media_dir == 'media':
            # Iterate over the posts directory
            for post_dir in os.listdir(os.path.join(root_dir, media_dir)):
                # Check if the post directory is a file
                if os.path.isfile(os.path.join(root_dir, media_dir, post_dir)):
                    # Check if the file is a JSON file
                    if post_dir.endswith('.json'):
                        # Open the JSON file
                        with open(os.path.join(root_dir, media_dir, post_dir), 'r') as file:
                            # Read the JSON file
                            data = file.read()
                            # Check if the JSON file contains the required data
                            if 'posts' in data:
                                # Extract the post views and video views
                                post_views[-1] += 1
                            elif 'reels' in data:
                                # Extract the post views and video views
                                video_views[-1] += 1
                            elif 'stories' in data:
                                # Extract the post views and video views
                                post_views[-1] += 1
                                video_views[-1] += 1

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    for i in range(len(accounts)):
        writer.writerow([accounts[i], post_views[i], video_views[i]])

print("The CSV file has been created successfully.")