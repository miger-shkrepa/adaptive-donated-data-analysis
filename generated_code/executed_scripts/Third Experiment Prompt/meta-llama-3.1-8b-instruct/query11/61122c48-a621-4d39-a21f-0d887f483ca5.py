import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the 'ads_information' directory
for file in os.listdir(os.path.join(root_dir, "ads_information")):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "ads_information", file), "r") as f:
            data = json.load(f)
            # Check if the file contains the required data
            if "ads_viewed.json" in data and "posts_viewed.json" in data and "likes.json" in data:
                # Extract the accounts from the 'ads_viewed.json' file
                ads_viewed_accounts = [item["string_map_data"]["Author"]["value"] for item in data["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]]
                # Extract the accounts from the 'posts_viewed.json' file
                posts_viewed_accounts = [item["string_map_data"]["Author"]["value"] for item in data["posts_viewed.json"]["structure"]["impressions_history_posts_seen"]]
                # Extract the accounts from the 'likes.json' file
                likes_accounts = [item["string_list_data"][0]["value"] for item in data["likes.json"]["structure"]["likes_media_likes"]]
                # Find the accounts that have viewed posts but not liked them
                accounts.extend([account for account in posts_viewed_accounts if account not in likes_accounts])

# Write the accounts to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])