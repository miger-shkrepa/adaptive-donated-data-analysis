import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement count for each user
engagement_count = {}

# Define a list of story engagement JSON files
story_engagement_files = [
    "story_likes.json",
    "story_reaction_sticker_reactions.json",
    "polls.json",
    "questions.json",
    "quizzes.json"
]

# Iterate over each file
for file in story_engagement_files:
    file_path = os.path.join(root_dir, "media", "stories", file)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning: The file {file} does not exist. Skipping this file.")
        continue

    # Load the JSON data
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the user and engagement count from the data
    for item in data["structure"]["story_activities_" + file.split(".")[0]]:
        user = item["title"]
        engagement = len(item["string_list_data"])

        # Update the engagement count for the user
        if user in engagement_count:
            engagement_count[user] += engagement
        else:
            engagement_count[user] = engagement

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, count in engagement_count.items():
        writer.writerow([user, count])