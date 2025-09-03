import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store user engagement data
user_engagement = {}

# Define the path to the story_likes.json file
story_likes_path = os.path.join(root_dir, "stories", "story_likes.json")

# Check if the story_likes.json file exists
if os.path.exists(story_likes_path):
    # Load the data from the story_likes.json file
    with open(story_likes_path, 'r') as f:
        data = json.load(f)

    # Iterate over the story_activities_story_likes list
    for story_like in data["story_activities_story_likes"]:
        # Extract the user from the title
        user = story_like["title"]

        # Extract the number of times the user engaged with the story
        times_engaged = len(story_like["string_list_data"])

        # Update the user engagement data
        if user in user_engagement:
            user_engagement[user] += times_engaged
        else:
            user_engagement[user] = times_engaged

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, times_engaged in user_engagement.items():
        writer.writerow([user, times_engaged])