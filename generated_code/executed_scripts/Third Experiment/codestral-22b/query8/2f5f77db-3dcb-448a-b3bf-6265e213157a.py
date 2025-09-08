import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = {}

# Define the JSON files to be processed
files = ["posts/post_likes.json", "story_activities/story_likes.json", "story_activities/story_reaction_sticker_reactions.json"]

# Process each file
for file in files:
    file_path = os.path.join(root_dir, file)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning: The file {file_path} does not exist. Skipping this file.")
        continue

    # Load the JSON data
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the user interactions
    for item in data:
        for interaction in item["string_list_data"]:
            user = interaction["value"]
            if user not in interactions:
                interactions[user] = 0
            interactions[user] += 1

# Sort the interactions in descending order
sorted_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Interactions"])
    for user, count in sorted_interactions[:20]:
        writer.writerow([user, count])