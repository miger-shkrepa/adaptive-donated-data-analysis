import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Define the path to the story interactions directory
story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Initialize a dictionary to store user engagement counts
user_engagement_counts = defaultdict(int)

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Check if the story interactions directory exists
if not os.path.exists(story_interactions_dir):
    raise FileNotFoundError("FileNotFoundError: The story interactions directory does not exist.")

# List of story interaction sections to process
story_sections = [
    "story_activities_emoji_sliders",
    "story_activities_emoji_quick_reactions",
    "story_activities_polls",
    "story_activities_questions",
    "story_activities_quizzes",
    "story_activities_story_likes",
    "story_activities_reaction_sticker_reactions"
]

# Process each JSON file in the story interactions directory
for filename in os.listdir(story_interactions_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(story_interactions_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for section in story_sections:
                    if section in data:
                        for entry in data[section]:
                            user = entry.get("title")
                            if user:
                                times_engaged = len(entry.get("string_list_data", []))
                                user_engagement_counts[user] += times_engaged
        except (FileNotFoundError, ValueError) as e:
            print(f"Error processing file {file_path}: {e}")

# Write the results to a CSV file
try:
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["User", "Times Engaged"])
        for user, times_engaged in user_engagement_counts.items():
            csvwriter.writerow([user, times_engaged])
except Exception as e:
    raise Exception(f"Error: Failed to write to the output CSV file. {e}")