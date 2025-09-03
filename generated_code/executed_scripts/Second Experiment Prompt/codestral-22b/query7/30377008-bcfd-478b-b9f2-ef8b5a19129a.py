import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagements = {}

# List of story interaction files
story_interaction_files = [
    "emoji_sliders.json",
    "emoji_story_reactions.json",
    "polls.json",
    "questions.json",
    "quizzes.json",
    "story_likes.json",
    "story_reaction_sticker_reactions.json"
]

# Iterate over each file
for file in story_interaction_files:
    file_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", file)

    # Skip if file does not exist
    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract usernames and engagement counts
    for item in data.get("story_activities_" + file.split(".")[0], []):
        username = item["title"]
        engagements[username] = engagements.get(username, 0) + len(item["string_list_data"])

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, count in engagements.items():
        writer.writerow([user, count])