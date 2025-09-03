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

# Function to process story interaction files
def process_story_interaction_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data.get("story_activities_" + os.path.basename(file_path).split('.')[0], []):
                for engagement in item.get("string_list_data", []):
                    user = engagement.get("value", "Unknown")
                    if user in engagements:
                        engagements[user] += 1
                    else:
                        engagements[user] = 1
    except FileNotFoundError:
        pass

# Process each story interaction file
for file_name in story_interaction_files:
    file_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", file_name)
    process_story_interaction_file(file_path)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, times_engaged in engagements.items():
        writer.writerow([user, times_engaged])