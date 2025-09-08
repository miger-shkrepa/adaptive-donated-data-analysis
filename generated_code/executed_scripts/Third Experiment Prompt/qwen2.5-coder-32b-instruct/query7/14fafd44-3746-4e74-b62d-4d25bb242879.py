import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Initialize a dictionary to count engagements per user
engagement_counts = defaultdict(int)

# Define the path to the story interactions directory
story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")

# Check if the story interactions directory exists
if not os.path.exists(story_interactions_dir):
    # If the directory does not exist, create an empty CSV file with headers
    os.makedirs('query_responses', exist_ok=True)
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
    raise FileNotFoundError("FileNotFoundError: The story interactions directory does not exist.")

# List of files to check for story interactions
interaction_files = [
    "emoji_story_reactions.json",
    "polls.json",
    "questions.json",
    "quizzes.json",
    "story_likes.json",
    "story_reaction_sticker_reactions.json"
]

# Process each interaction file
for interaction_file in interaction_files:
    file_path = os.path.join(story_interactions_dir, interaction_file)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        continue  # Skip the file if it does not exist
    
    try:
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the relevant data based on the file type
        if interaction_file == "emoji_story_reactions.json":
            activities = data.get("story_activities_emoji_quick_reactions", [])
        elif interaction_file == "polls.json":
            activities = data.get("story_activities_polls", [])
        elif interaction_file == "questions.json":
            activities = data.get("story_activities_questions", [])
        elif interaction_file == "quizzes.json":
            activities = data.get("story_activities_quizzes", [])
        elif interaction_file == "story_likes.json":
            activities = data.get("story_activities_story_likes", [])
        elif interaction_file == "story_reaction_sticker_reactions.json":
            activities = data.get("story_activities_reaction_sticker_reactions", [])
        else:
            continue  # Skip if the file type is not recognized
        
        # Count engagements per user
        for activity in activities:
            for item in activity.get("string_list_data", []):
                user = item.get("value")
                if user:
                    engagement_counts[user] += 1
    
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error decoding JSON in {interaction_file}: {str(e)}")
    except Exception as e:
        raise ValueError(f"ValueError: Error processing {interaction_file}: {str(e)}")

# Sort the engagement counts by the number of engagements in descending order
sorted_engagements = sorted(engagement_counts.items(), key=lambda x: x[1], reverse=True)

# Write the results to a CSV file
os.makedirs('query_responses', exist_ok=True)
with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Times Engaged'])
    for user, count in sorted_engagements:
        writer.writerow([user, count])