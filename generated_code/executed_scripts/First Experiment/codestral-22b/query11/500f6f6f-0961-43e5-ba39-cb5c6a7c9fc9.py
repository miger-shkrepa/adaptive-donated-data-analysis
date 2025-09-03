import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty set to store the accounts that have been viewed but not liked
viewed_but_not_liked = set()

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "posts_1.json":
            # Open the posts_1.json file
            with open(os.path.join(foldername, filename), 'r') as f:
                data = json.load(f)
                # Extract the accounts from the posts
                for post in data['media']:
                    account = post['title']
                    viewed_but_not_liked.add(account)
        elif filename == "liked_posts.json":
            # Open the liked_posts.json file
            with open(os.path.join(foldername, filename), 'r') as f:
                data = json.load(f)
                # Extract the accounts from the liked posts
                for liked_post in data['likes_media_likes']:
                    account = liked_post['title']
                    if account in viewed_but_not_liked:
                        viewed_but_not_liked.remove(account)

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in viewed_but_not_liked:
        writer.writerow([account])