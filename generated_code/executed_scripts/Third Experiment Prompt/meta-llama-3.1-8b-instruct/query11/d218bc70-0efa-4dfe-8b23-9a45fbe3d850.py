import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the set of accounts that have viewed posts but not liked them
accounts_viewed_but_not_liked = set()

# Iterate over the JSON files in the 'your_instagram_activity' directory
for filename in os.listdir(os.path.join(root_dir, "your_instagram_activity")):
    if filename.endswith(".json"):
        with open(os.path.join(root_dir, "your_instagram_activity", filename), "r") as file:
            data = json.load(file)
            # Check if the file contains the 'likes' and 'media' structures
            if "likes" in data and "media" in data:
                # Iterate over the 'likes' structure
                for liked_post in data["likes"]["liked_posts"]["likes_media_likes"]:
                    # Check if the post has a 'title' and a 'string_list_data' with a 'value' that is not empty
                    if "title" in liked_post and "string_list_data" in liked_post and liked_post["string_list_data"]:
                        # Add the account to the set
                        accounts_viewed_but_not_liked.add(liked_post["title"])
            # Check if the file contains the 'media' structure
            if "media" in data:
                # Iterate over the 'media' structure
                for post in data["media"]["posts_1"]["structure"]:
                    # Check if the post has a 'title' and a 'media' with a 'creation_timestamp' that is not empty
                    if "title" in post and "media" in post and post["media"]:
                        # Check if the post has a 'creation_timestamp' that is not empty
                        if "creation_timestamp" in post["media"][0]:
                            # Check if the post has a 'title' that is not in the set of accounts that have liked posts
                            if post["title"] not in accounts_viewed_but_not_liked:
                                # Add the account to the set
                                accounts_viewed_but_not_liked.add(post["title"])

# Write the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])
    for account in accounts_viewed_but_not_liked:
        writer.writerow([account])