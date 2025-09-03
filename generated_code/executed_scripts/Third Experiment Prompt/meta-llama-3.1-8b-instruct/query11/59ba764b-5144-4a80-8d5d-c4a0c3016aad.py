import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Iterate over the JSON files in the 'ads_information' directory
for filename in os.listdir(os.path.join(root_dir, "ads_information")):
    if filename.endswith(".json"):
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, "ads_information", filename), "r") as f:
            data = json.load(f)

        # Check if the JSON file contains the required data
        if "ads_and_topics" in data and "posts_viewed.json" in data["ads_and_topics"]:
            # Load the posts_viewed.json file
            posts_viewed_data = data["ads_and_topics"]["posts_viewed.json"]

            # Iterate over the posts_viewed.json file
            for post in posts_viewed_data["structure"]["impressions_history_posts_seen"]:
                # Check if the post has a string_map_data with an "Author" key
                if "string_map_data" in post and "Author" in post["string_map_data"]:
                    # Get the author's name
                    author = post["string_map_data"]["Author"]["value"]

                    # Iterate over the JSON files in the 'connections' directory
                    for filename in os.listdir(os.path.join(root_dir, "connections")):
                        if filename.endswith(".json"):
                            # Open the JSON file and load its contents
                            with open(os.path.join(root_dir, "connections", filename), "r") as f:
                                data = json.load(f)

                            # Check if the JSON file contains the required data
                            if "followers_and_following" in data and "accounts_you've_favorited.json" in data["followers_and_following"]:
                                # Load the accounts_you've_favorited.json file
                                accounts_favorited_data = data["followers_and_following"]["accounts_you've_favorited.json"]

                                # Iterate over the accounts_you've_favorited.json file
                                for account in accounts_favorited_data["structure"]["relationships_feed_favorites"]:
                                    # Check if the account has a string_list_data with a value that matches the author's name
                                    if "string_list_data" in account and any(value["value"] == author for value in account["string_list_data"]):
                                        # Add the account to the results list
                                        results.append(author)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the column headers
    for result in results:
        writer.writerow([result])