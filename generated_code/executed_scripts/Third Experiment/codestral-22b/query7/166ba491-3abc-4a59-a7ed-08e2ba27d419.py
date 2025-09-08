import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the engagement data
engagement_data = {}

# Define the path to the story_likes.json file
story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")

# Check if the story_likes.json file exists
if os.path.exists(story_likes_path):
    # Load the data from the story_likes.json file
    with open(story_likes_path, "r") as f:
        data = json.load(f)

    # Iterate over the story_activities_story_likes list
    for story_like in data["story_activities_story_likes"]:
        # Extract the user from the title
        user = story_like["title"]

        # Extract the number of times the user engaged with the story
        times_engaged = len(story_like["string_list_data"])

        # Update the engagement data dictionary
        if user in engagement_data:
            engagement_data[user] += times_engaged
        else:
            engagement_data[user] = times_engaged

# Define the path to the results.csv file
results_path = "query_responses/results.csv"

# Write the engagement data to the results.csv file
with open(results_path, "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data rows
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])