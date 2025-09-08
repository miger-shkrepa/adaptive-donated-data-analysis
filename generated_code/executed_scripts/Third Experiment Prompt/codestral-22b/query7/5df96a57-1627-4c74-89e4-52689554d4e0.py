import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement data
engagement_data = {}

# Define the path to the story likes data
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")

# Check if the story likes file exists
if os.path.exists(story_likes_path):
    # Open the story likes file
    with open(story_likes_path, "r") as f:
        # Load the story likes data
        story_likes_data = json.load(f)

        # Iterate over the story likes data
        for story_like in story_likes_data["story_activities_story_likes"]:
            # Extract the user name
            user = story_like["title"]

            # Extract the number of story likes
            likes = len(story_like["string_list_data"])

            # Update the engagement data
            if user in engagement_data:
                engagement_data[user] += likes
            else:
                engagement_data[user] = likes

# Define the path to the output file
output_path = "query_responses/results.csv"

# Open the output file
with open(output_path, "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])