import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = 'query_responses/results.csv'

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])

    # Iterate over the directory structure
    for user in os.listdir(root_dir):
        user_dir = os.path.join(root_dir, user)
        if os.path.isdir(user_dir):
            story_interactions_file = os.path.join(user_dir, "story_interactions", "story_reaction_sticker_reactions.json")
            if os.path.exists(story_interactions_file):
                with open(story_interactions_file, 'r') as f:
                    data = json.load(f)
                    story_interactions = data["story_activities_reaction_sticker_reactions"]
                    user_engagements = 0
                    for interaction in story_interactions:
                        user_engagements += len(interaction["string_list_data"])
                    writer.writerow([user, user_engagements])
            else:
                writer.writerow([user, 0])