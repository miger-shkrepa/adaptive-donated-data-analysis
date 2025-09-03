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

# Define the path to the liked posts JSON file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Check if the liked posts JSON file exists
if os.path.exists(liked_posts_path):
    # Load the liked posts data
    with open(liked_posts_path, 'r') as f:
        liked_posts_data = json.load(f)

    # Extract the accounts from the liked posts data
    liked_accounts = set(post['title'] for post in liked_posts_data['likes_media_likes'])
else:
    liked_accounts = set()

# Define the path to the saved posts JSON file
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Check if the saved posts JSON file exists
if os.path.exists(saved_posts_path):
    # Load the saved posts data
    with open(saved_posts_path, 'r') as f:
        saved_posts_data = json.load(f)

    # Extract the accounts from the saved posts data
    saved_accounts = set(post['title'] for post in saved_posts_data['saved_saved_media'])
else:
    saved_accounts = set()

# Find the accounts that have saved posts but not liked them
accounts = saved_accounts - liked_accounts

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in accounts:
        writer.writerow([account])