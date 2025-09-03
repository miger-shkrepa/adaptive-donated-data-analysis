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
    # Open the posts_viewed.json file
    with open(posts_viewed_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the accounts from the JSON data
        for post in data["impressions_history_posts_seen"]:
            account = post["string_map_data"]["Author"]["value"]
            accounts.append(account)

# Define the path to the liked_posts.json file
liked_posts_file = os.path.join(root_dir, "liked_posts.json")

# Check if the liked_posts.json file exists
if os.path.exists(liked_posts_file):
    # Open the liked_posts.json file
    with open(liked_posts_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the accounts from the JSON data
        liked_accounts = [post["string_map_data"]["Author"]["value"] for post in data["liked_posts"]]

        # Remove the liked accounts from the accounts list
        accounts = [account for account in accounts if account not in liked_accounts]

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])