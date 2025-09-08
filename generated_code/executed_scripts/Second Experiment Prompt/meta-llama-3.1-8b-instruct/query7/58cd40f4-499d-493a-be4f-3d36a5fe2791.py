import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the user engagement dictionary
user_engagement = {}

# Iterate over the directory structure
for dir_path, dir_names, file_names in os.walk(root_dir):
    # Iterate over the files in the current directory
    for file_name in file_names:
        # Check if the file is a JSON file
        if file_name.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(dir_path, file_name), "r") as file:
                # Load the JSON data
                data = json.load(file)
                # Check if the JSON data has a 'story_activities' key
                if "story_activities" in data:
                    # Iterate over the story activities
                    for story_activity in data["story_activities"]:
                        # Check if the story activity has a 'story_likes' key
                        if "story_likes" in story_activity:
                            # Iterate over the story likes
                            for story_like in story_activity["story_likes"]:
                                # Get the user who liked the story
                                user = story_like["title"]
                                # Get the timestamp of the story like
                                timestamp = story_like["timestamp"]
                                # Increment the user's engagement count
                                if user in user_engagement:
                                    user_engagement[user] += 1
                                else:
                                    user_engagement[user] = 1

# Sort the user engagement dictionary by value in descending order
sorted_user_engagement = dict(sorted(user_engagement.items(), key=lambda item: item[1], reverse=True))

# Write the user engagement data to a CSV file
with open("query_responses/results.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    # Write the column headers
    writer.writerow(["User", "Times Engaged"])
    # Write the user engagement data
    for user, engagement in sorted_user_engagement.items():
        writer.writerow([user, engagement])