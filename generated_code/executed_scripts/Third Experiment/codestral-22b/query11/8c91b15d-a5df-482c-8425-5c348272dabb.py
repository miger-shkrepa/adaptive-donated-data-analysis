import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Define the path to the liked_posts.json file
liked_posts_path = os.path.join(root_dir, 'likes', 'liked_posts.json')

# Check if the liked_posts.json file exists
if os.path.exists(liked_posts_path):
    # Load the liked_posts.json file
    with open(liked_posts_path, 'r') as f:
        liked_posts = json.load(f)

    # Extract the accounts from the liked_posts.json file
    liked_accounts = set(post['title'] for post in liked_posts['likes_media_likes'])
else:
    liked_accounts = set()

# Define the path to the recently_viewed_items.json file
recently_viewed_items_path = os.path.join(root_dir, 'shopping', 'recently_viewed_items.json')

# Check if the recently_viewed_items.json file exists
if os.path.exists(recently_viewed_items_path):
    # Load the recently_viewed_items.json file
    with open(recently_viewed_items_path, 'r') as f:
        recently_viewed_items = json.load(f)

    # Extract the accounts from the recently_viewed_items.json file
    viewed_accounts = set(item['string_map_data']['Merchant Name']['value'] for item in recently_viewed_items['checkout_saved_recently_viewed_products'])
else:
    viewed_accounts = set()

# Find the accounts that the user has viewed but not liked
unliked_accounts = viewed_accounts - liked_accounts

# Add the accounts to the list
accounts.extend(unliked_accounts)

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in accounts:
        writer.writerow([account])