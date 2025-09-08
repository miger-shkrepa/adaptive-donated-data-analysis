import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty set to store the accounts that the user has viewed but not liked
viewed_but_not_liked = set()

# Define the path to the saved posts JSON file
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Check if the saved posts JSON file exists
if os.path.exists(saved_posts_path):
    # Open the saved posts JSON file
    with open(saved_posts_path, "r") as f:
        # Load the JSON data
        saved_posts = json.load(f)

    # Extract the accounts from the saved posts
    saved_accounts = {post["title"] for post in saved_posts["saved_saved_media"]}

    # Define the path to the liked posts JSON file
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    # Check if the liked posts JSON file exists
    if os.path.exists(liked_posts_path):
        # Open the liked posts JSON file
        with open(liked_posts_path, "r") as f:
            # Load the JSON data
            liked_posts = json.load(f)

        # Extract the accounts from the liked posts
        liked_accounts = {post["title"] for post in liked_posts["likes_media_likes"]}

        # Find the accounts that the user has viewed but not liked
        viewed_but_not_liked = saved_accounts - liked_accounts

# Define the path to the output CSV file
output_path = "query_responses/results.csv"

# Create the directory for the output CSV file if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the results to a CSV file
with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    for account in viewed_but_not_liked:
        writer.writerow([account])