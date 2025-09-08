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

# Define the path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_path):
    # Open the posts_viewed.json file
    with open(posts_viewed_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the accounts from the JSON data
        viewed_accounts = [item["string_map_data"]["Author"]["value"] for item in data["impressions_history_posts_seen"]]

    # Define the path to the story_likes.json file
    story_likes_path = os.path.join(root_dir, "connections", "story_interactions", "story_likes.json")

    # Check if the story_likes.json file exists
    if os.path.exists(story_likes_path):
        # Open the story_likes.json file
        with open(story_likes_path, "r") as f:
            # Load the JSON data
            data = json.load(f)

            # Extract the accounts from the JSON data
            liked_accounts = [item["title"] for item in data["story_activities_story_likes"]]

        # Find the accounts that have been viewed but not liked
        accounts = [account for account in viewed_accounts if account not in liked_accounts]

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])