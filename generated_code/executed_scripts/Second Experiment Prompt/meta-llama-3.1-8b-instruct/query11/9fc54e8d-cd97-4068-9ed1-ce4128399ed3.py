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

# Iterate over the subdirectories in the root directory
for dir_name in os.listdir(root_dir):
    dir_path = os.path.join(root_dir, dir_name)
    if os.path.isdir(dir_path):
        # Check if the subdirectory contains the required files
        likes_file = os.path.join(dir_path, "likes", "liked_posts.json")
        saved_file = os.path.join(dir_path, "saved", "saved_posts.json")
        if os.path.exists(likes_file) and os.path.exists(saved_file):
            # Load the JSON files
            with open(likes_file, "r") as f:
                likes_data = json.load(f)
            with open(saved_file, "r") as f:
                saved_data = json.load(f)

            # Extract the account names from the likes data
            account_names = set()
            for post in likes_data["structure"]["likes_media_likes"]:
                account_names.add(post["title"])

            # Extract the account names from the saved data
            for post in saved_data["structure"]["saved_saved_media"]:
                account_names.add(post["title"])

            # Find the accounts that have viewed posts but not liked them
            viewed_but_not_liked = [name for name in account_names if name not in [post["title"] for post in likes_data["structure"]["likes_media_likes"]]]

            # Add the results to the list
            results.extend(viewed_but_not_liked)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the header
    writer.writerows([[account] for account in results])