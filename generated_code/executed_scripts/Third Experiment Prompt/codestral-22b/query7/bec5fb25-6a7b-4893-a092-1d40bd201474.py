import os
import json
import csv
from datetime import datetime
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement data
engagement_data = defaultdict(int)

# Define the path to the story interactions directory
story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")

# Check if the story interactions directory exists
if not os.path.exists(story_interactions_dir):
    print("Warning: The story interactions directory does not exist.")
else:
    # Define the path to the story likes file
    story_likes_file = os.path.join(story_interactions_dir, "story_likes.json")

    # Check if the story likes file exists
    if not os.path.exists(story_likes_file):
        print("Warning: The story likes file does not exist.")
    else:
        # Load the story likes data
        with open(story_likes_file, "r") as f:
            story_likes_data = json.load(f)

        # Extract the engagement data
        for item in story_likes_data.get("story_activities_story_likes", []):
            user = item.get("title", "")
            engagement_data[user] += len(item.get("string_list_data", []))

# Write the engagement data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Times Engaged"])
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])