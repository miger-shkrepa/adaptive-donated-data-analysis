import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement count for each user
engagement_count = {}

# Define the path to the story_likes.json file
story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")

# Check if the story_likes.json file exists
if os.path.exists(story_likes_path):
    # Open the story_likes.json file
    with open(story_likes_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the story_activities_story_likes list
        for story in data["story_activities_story_likes"]:
            # Iterate over the string_list_data list
            for engagement in story["string_list_data"]:
                # Extract the user from the href
                user = engagement["href"].split("/")[-2]

                # Increment the engagement count for the user
                if user in engagement_count:
                    engagement_count[user] += 1
                else:
                    engagement_count[user] = 1

# Define the path to the countdowns.json file
countdowns_path = os.path.join(root_dir, "story_interactions", "countdowns.json")

# Check if the countdowns.json file exists
if os.path.exists(countdowns_path):
    # Open the countdowns.json file
    with open(countdowns_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the story_activities_countdowns list
        for story in data["story_activities_countdowns"]:
            # Iterate over the string_list_data list
            for engagement in story["string_list_data"]:
                # Extract the user from the href
                user = engagement["href"].split("/")[-2]

                # Increment the engagement count for the user
                if user in engagement_count:
                    engagement_count[user] += 1
                else:
                    engagement_count[user] = 1

# Create a list of tuples containing the user and engagement count
engagement_list = [(user, count) for user, count in engagement_count.items()]

# Sort the list in descending order of engagement count
engagement_list.sort(key=lambda x: x[1], reverse=True)

# Define the path to the results.csv file
results_path = "query_responses/results.csv"

# Open the results.csv file in write mode
with open(results_path, "w", newline="") as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data rows
    writer.writerows(engagement_list)