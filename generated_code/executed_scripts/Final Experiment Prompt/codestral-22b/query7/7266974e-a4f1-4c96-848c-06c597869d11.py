import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the results
results = {}

# Define the story interaction sections
story_interactions = ["story_activities_emoji_sliders", "story_activities_emoji_quick_reactions",
                      "story_activities_polls", "story_activities_questions", "story_activities_quizzes",
                      "story_activities_story_likes", "story_activities_reaction_sticker_reactions"]

# Iterate over the story interaction sections
for section in story_interactions:
    # Define the path to the section directory
    section_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions", section)

    # Check if the section directory exists
    if not os.path.exists(section_dir):
        continue

    # Iterate over the JSON files in the section directory
    for filename in os.listdir(section_dir):
        if filename.endswith(".json"):
            # Define the path to the JSON file
            file_path = os.path.join(section_dir, filename)

            # Open the JSON file
            with open(file_path, "r") as f:
                # Load the JSON data
                data = json.load(f)

                # Iterate over the entries in the data
                for entry in data:
                    # Extract the user and times engaged
                    user = entry["title"]
                    times_engaged = len(entry["string_list_data"])

                    # Update the results dictionary
                    if user in results:
                        results[user] += times_engaged
                    else:
                        results[user] = times_engaged

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(["User", "Times Engaged"])

    # Write the results
    for user, times_engaged in results.items():
        writer.writerow([user, times_engaged])