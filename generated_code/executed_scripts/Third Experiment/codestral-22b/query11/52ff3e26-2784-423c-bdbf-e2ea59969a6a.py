import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Navigate to the 'story_activities' directory
story_activities_dir = os.path.join(root_dir, 'story_activities')
if not os.path.exists(story_activities_dir):
    print("Warning: The 'story_activities' directory does not exist. Skipping this part of the query.")
else:
    # Load the 'story_likes.json' file
    story_likes_file = os.path.join(story_activities_dir, 'story_likes.json')
    if not os.path.exists(story_likes_file):
        print("Warning: The 'story_likes.json' file does not exist. Skipping this part of the query.")
    else:
        with open(story_likes_file, 'r') as f:
            story_likes = json.load(f)

        # Extract the accounts that have liked posts
        liked_accounts = {item['title'] for item in story_likes['structure']['story_activities_story_likes']}

    # Load the 'posts.json' file
    posts_file = os.path.join(story_activities_dir, 'posts.json')
    if not os.path.exists(posts_file):
        print("Warning: The 'posts.json' file does not exist. Skipping this part of the query.")
    else:
        with open(posts_file, 'r') as f:
            posts = json.load(f)

        # Extract the accounts that have viewed posts
        viewed_accounts = {item['title'] for item in posts['structure']['story_activities_posts']}

        # Find the accounts that have viewed posts but not liked them
        accounts = list(viewed_accounts - liked_accounts)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in accounts:
        writer.writerow([account])