import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagements = {}

# Define the JSON files we're interested in
story_files = [
    "emoji_sliders.json",
    "emoji_story_reactions.json",
    "polls.json",
    "questions.json",
    "quizzes.json",
    "story_likes.json",
    "story_reaction_sticker_reactions.json"
]

# Iterate over the story files
for file in story_files:
    file_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", file)

    # If the file doesn't exist, skip it
    if not os.path.exists(file_path):
        continue

    with open(file_path, "r") as f:
        data = json.load(f)

    # Extract the user and engagement data
    for item in data.values():
        for engagement in item:
            user = engagement["title"]
            times = len(engagement["string_list_data"])

            if user in engagements:
                engagements[user] += times
            else:
                engagements[user] = times

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Times Engaged"])

    for user, times in engagements.items():
        writer.writerow([user, times])