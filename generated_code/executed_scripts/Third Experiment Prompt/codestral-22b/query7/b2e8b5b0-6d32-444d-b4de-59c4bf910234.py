import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement data
engagement_data = {}

# Define the path to the liked posts JSON file
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Check if the liked posts JSON file exists
if os.path.exists(liked_posts_path):
    # Open the liked posts JSON file
    with open(liked_posts_path, "r") as f:
        # Load the JSON data
        liked_posts_data = json.load(f)

        # Iterate over the liked posts
        for post in liked_posts_data["likes_media_likes"]:
            # Extract the user from the post title
            user = post["title"].split("'s")[0]

            # If the user is not in the engagement data, add them
            if user not in engagement_data:
                engagement_data[user] = 0

            # Increment the user's engagement count
            engagement_data[user] += 1

# Define the path to the saved posts JSON file
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Check if the saved posts JSON file exists
if os.path.exists(saved_posts_path):
    # Open the saved posts JSON file
    with open(saved_posts_path, "r") as f:
        # Load the JSON data
        saved_posts_data = json.load(f)

        # Iterate over the saved posts
        for post in saved_posts_data["saved_saved_media"]:
            # Extract the user from the post title
            user = post["title"].split("'s")[0]

            # If the user is not in the engagement data, add them
            if user not in engagement_data:
                engagement_data[user] = 0

            # Increment the user's engagement count
            engagement_data[user] += 1

# Write the engagement data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])