import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement count for each user
engagement_count = {}

# Define the path to the story_likes.json file
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")

# Check if the story_likes.json file exists
if os.path.exists(story_likes_path):
    # Load the story_likes.json file
    with open(story_likes_path, "r") as f:
        story_likes_data = json.load(f)

    # Iterate over the story_activities_story_likes list
    for story_like in story_likes_data["story_activities_story_likes"]:
        # Extract the user from the title
        user = story_like["title"]

        # Update the engagement count for the user
        if user in engagement_count:
            engagement_count[user] += 1
        else:
            engagement_count[user] = 1

# Define the path to the results.csv file
results_path = "query_responses/results.csv"

# Write the results to the results.csv file
with open(results_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Times Engaged"])
    for user, count in engagement_count.items():
        writer.writerow([user, count])