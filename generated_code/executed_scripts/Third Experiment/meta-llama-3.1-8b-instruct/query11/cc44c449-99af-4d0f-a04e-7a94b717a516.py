import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the required data
            if "story_likes.json" in data and "posts_viewed.json" in data:
                # Extract the accounts from the posts_viewed.json file
                posts_viewed_accounts = [post["string_map_data"]["Author"]["value"] for post in data["posts_viewed.json"]["structure"]["impressions_history_posts_seen"][0]["string_map_data"].values() if "Author" in post]

                # Extract the accounts from the story_likes.json file
                story_likes_accounts = [like["string_list_data"][0]["value"] for like in data["story_likes.json"]["structure"]["story_activities_story_likes"][0]["string_list_data"] if "value" in like]

                # Find the accounts that have viewed posts but not liked them
                accounts.extend([account for account in posts_viewed_accounts if account not in story_likes_accounts])

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the column headers
    writer.writerows([[account] for account in accounts])  # Write the accounts