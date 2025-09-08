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

# Construct the path to the story_likes.json file
story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")

# Check if the story_likes.json file exists
if os.path.exists(story_likes_path):
    # Open the story_likes.json file
    with open(story_likes_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Check if the data has the expected structure
        if "story_activities_story_likes" in data:
            # Iterate over the story likes
            for story_like in data["story_activities_story_likes"]:
                # Extract the user's name
                user = story_like["title"]

                # Count the number of times the user's story has been liked
                likes = len(story_like["string_list_data"])

                # Add the data to the engagement_data dictionary
                if user in engagement_data:
                    engagement_data[user] += likes
                else:
                    engagement_data[user] = likes

# Write the engagement data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])