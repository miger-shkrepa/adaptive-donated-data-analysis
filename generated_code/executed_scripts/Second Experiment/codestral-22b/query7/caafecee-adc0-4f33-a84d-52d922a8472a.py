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

# Define the path to the stories file
stories_file = os.path.join(root_dir, "media", "posts_1.json")

# Check if the stories file exists
if os.path.exists(stories_file):
    # Open the stories file
    with open(stories_file, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the stories
        for story in data["media"]:
            # Extract the user who posted the story
            user = story["title"]

            # If the user is not in the engagement count dictionary, add them
            if user not in engagement_count:
                engagement_count[user] = 0

            # Increment the engagement count for the user
            engagement_count[user] += 1

# Create a list of tuples containing the user and their engagement count
engagement_list = [(user, count) for user, count in engagement_count.items()]

# Sort the list in descending order of engagement count
engagement_list.sort(key=lambda x: x[1], reverse=True)

# Define the path to the output file
output_file = "query_responses/results.csv"

# Open the output file in write mode
with open(output_file, "w", newline="") as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the engagement data
    writer.writerows(engagement_list)