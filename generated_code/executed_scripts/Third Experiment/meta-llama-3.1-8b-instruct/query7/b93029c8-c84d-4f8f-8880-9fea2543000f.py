import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionary to store the engagement counts
engagement_counts = {}

# Iterate over the JSON files in the 'story_interactions' directory
for filename in os.listdir(root_dir):
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)
            # Iterate over the story likes
            for story_like in parsed_data['story_activities_story_likes']:
                # Get the user who liked the story
                user = story_like['title']
                # Increment the engagement count for the user
                engagement_counts[user] = engagement_counts.get(user, 0) + 1

# Initialize the list to store the CSV rows
csv_rows = [['User', 'Times Engaged']]

# Iterate over the engagement counts
for user, count in engagement_counts.items():
    # Append the user and engagement count to the CSV rows
    csv_rows.append([user, count])

# Write the CSV rows to the output file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_rows)