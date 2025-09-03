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

# Define the path to the posts_viewed.json file
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    # Load the JSON data from the posts_viewed.json file
    with open(posts_viewed_file, "r") as f:
        posts_viewed_data = json.load(f)

    # Extract the accounts from the posts_viewed data
    viewed_accounts = set(post["string_map_data"]["Author"]["value"] for post in posts_viewed_data["impressions_history_posts_seen"])

    # Define the path to the liked_posts.json file
    liked_posts_file = os.path.join(root_dir, "connections", "likes", "liked_posts.json")

    # Check if the liked_posts.json file exists
    if os.path.exists(liked_posts_file):
        # Load the JSON data from the liked_posts.json file
        with open(liked_posts_file, "r") as f:
            liked_posts_data = json.load(f)

        # Extract the accounts from the liked_posts data
        liked_accounts = set(post["string_list_data"][0]["value"] for post in liked_posts_data["likes_media_likes"])

        # Find the accounts that have been viewed but not liked
        accounts = list(viewed_accounts - liked_accounts)

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])