import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Check if the liked_posts.json file exists
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    # Load the liked_posts.json file
    with open(liked_posts_path, "r") as f:
        liked_posts = json.load(f)

    # Extract the profiles that the user has liked
    liked_profiles = set()
    for post in liked_posts["likes_media_likes"]:
        for data in post["string_list_data"]:
            liked_profiles.add(data["value"])

    # Check if the saved_posts.json file exists
    saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
    if os.path.exists(saved_posts_path):
        # Load the saved_posts.json file
        with open(saved_posts_path, "r") as f:
            saved_posts = json.load(f)

        # Extract the profiles that the user has saved
        saved_profiles = set()
        for post in saved_posts["saved_saved_media"]:
            saved_profiles.add(post["title"])

        # Find the profiles that the user follows but do not follow him back
        followed_profiles = liked_profiles.union(saved_profiles)
        unfollowed_profiles = followed_profiles.difference(liked_profiles)

        # Add the unfollowed profiles to the list
        profiles.extend(unfollowed_profiles)

# Save the results to a CSV file
output_path = "query_responses/results.csv"
with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])