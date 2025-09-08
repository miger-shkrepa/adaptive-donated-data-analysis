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
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    # Load the JSON data from the posts_viewed.json file
    with open(posts_viewed_file, "r") as f:
        posts_viewed_data = json.load(f)

    # Extract the accounts from the posts_viewed data
    viewed_accounts = set(post["string_map_data"]["Author"]["value"] for post in posts_viewed_data["impressions_history_posts_seen"])

    # Define the path to the following.json file
    following_file = os.path.join(root_dir, "connections", "followers_and_following", "following.json")

    # Check if the following.json file exists
    if os.path.exists(following_file):
        # Load the JSON data from the following.json file
        with open(following_file, "r") as f:
            following_data = json.load(f)

        # Extract the accounts from the following data
        following_accounts = set(account["string_list_data"][0]["value"] for account in following_data["relationships_following"])

        # Find the accounts that have been viewed but not liked
        accounts = list(viewed_accounts - following_accounts)

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])