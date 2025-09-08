import os
import json
import csv

# Declare the variable referring to the file input
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
    # If the directory does not exist, create a CSV file with only the column headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
else:
    # Iterate over the JSON files in the story interactions directory
    for filename in os.listdir(story_interactions_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(story_interactions_dir, filename)

            # Open the JSON file and load the data
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Extract the story activities data based on the filename
            if filename == "polls.json":
                story_activities = data.get("story_activities_polls", [])
            elif filename == "questions.json":
                story_activities = data.get("story_activities_questions", [])
            elif filename == "story_likes.json":
                story_activities = data.get("story_activities_story_likes", [])

            # Iterate over the story activities and update the engagement data
            for activity in story_activities:
                title = activity.get("title", "")
                if title:
                    if title in engagement_data:
                        engagement_data[title] += 1
                    else:
                        engagement_data[title] = 1

    # Write the engagement data to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, times_engaged in engagement_data.items():
            writer.writerow([user, times_engaged])