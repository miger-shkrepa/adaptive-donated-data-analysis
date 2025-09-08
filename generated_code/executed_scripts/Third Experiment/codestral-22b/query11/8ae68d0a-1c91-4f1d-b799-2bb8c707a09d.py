import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty set to store the accounts that have viewed posts but not liked them
accounts = set()

# Define the path to the posts_viewed.json file
posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    # Load the data from the posts_viewed.json file
    with open(posts_viewed_file, 'r') as f:
        posts_viewed_data = json.load(f)

    # Extract the accounts from the posts_viewed_data
    viewed_accounts = set(post['string_map_data']['Author']['value'] for post in posts_viewed_data['impressions_history_posts_seen'])

    # Define the path to the story_likes.json file
    story_likes_file = os.path.join(root_dir, 'story_interactions', 'story_likes.json')

    # Check if the story_likes.json file exists
    if os.path.exists(story_likes_file):
        # Load the data from the story_likes.json file
        with open(story_likes_file, 'r') as f:
            story_likes_data = json.load(f)

        # Extract the accounts from the story_likes_data
        liked_accounts = set(like['title'] for like in story_likes_data['story_activities_story_likes'])

        # Find the accounts that have viewed posts but not liked them
        accounts = viewed_accounts - liked_accounts

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])
    for account in accounts:
        writer.writerow([account])