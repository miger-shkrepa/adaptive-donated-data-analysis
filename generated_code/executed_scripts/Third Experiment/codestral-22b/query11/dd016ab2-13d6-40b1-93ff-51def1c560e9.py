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

# Navigate to the posts_viewed.json file
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    with open(posts_viewed_file, 'r') as f:
        posts_viewed = json.load(f)

    # Extract the accounts from the posts_viewed.json file
    accounts_viewed = [post['string_map_data']['Author']['value'] for post in posts_viewed['impressions_history_posts_seen']]

    # Navigate to the liked_posts.json file
    liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    # Check if the liked_posts.json file exists
    if os.path.exists(liked_posts_file):
        with open(liked_posts_file, 'r') as f:
            liked_posts = json.load(f)

        # Extract the accounts from the liked_posts.json file
        accounts_liked = [post['string_list_data'][0]['value'] for post in liked_posts['likes_media_likes']]

        # Find the accounts that have been viewed but not liked
        accounts = [account for account in accounts_viewed if account not in accounts_liked]

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in accounts:
        writer.writerow([account])