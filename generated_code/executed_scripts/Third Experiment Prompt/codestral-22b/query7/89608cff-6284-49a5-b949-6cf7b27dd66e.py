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
        # Open the story likes file
        with open(story_likes_file, "r") as f:
            # Load the JSON data
            data = json.load(f)

            # Iterate over the story likes data
            for item in data["story_activities_story_likes"]:
                # Extract the user
                user = item["title"]

                # Extract the number of times engaged
                times_engaged = len(item["string_list_data"])

                # Add the data to the engagement data dictionary
                if user in engagement_data:
                    engagement_data[user] += times_engaged
                else:
                    engagement_data[user] = times_engaged

# Write the engagement data to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])