import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the 'ads_information' directory
for file in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "ads_information", "ads_and_topics", file), "r") as f:
            data = json.load(f)
            # Check if the file contains the required structure
            if "ads_viewed.json" in data and "ads_and_topics" in data["ads_viewed.json"]["structure"]:
                # Extract the accounts from the file
                for item in data["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]:
                    if "string_map_data" in item and "Author" in item["string_map_data"] and "Time" in item["string_map_data"]:
                        # Check if the account has not liked the post
                        try:
                            with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "liked_posts.json"), "r") as liked_posts_file:
                                liked_posts_data = json.load(liked_posts_file)
                                if "ads_and_topics" in liked_posts_data["structure"] and "likes_media_likes" in liked_posts_data["structure"]["ads_and_topics"]:
                                    liked_posts = liked_posts_data["structure"]["ads_and_topics"]["likes_media_likes"]
                                    if not any(item["string_map_data"]["Author"]["value"] in post["string_list_data"][0]["value"] for post in liked_posts):
                                        accounts.append(item["string_map_data"]["Author"]["value"])
                        except FileNotFoundError:
                            # If the 'liked_posts.json' file does not exist, treat its contribution as 0
                            pass

# Write the accounts to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])
    writer.writerows([[account] for account in accounts])