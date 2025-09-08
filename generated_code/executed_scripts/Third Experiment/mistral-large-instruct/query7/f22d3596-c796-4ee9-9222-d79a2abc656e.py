import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store user engagement counts
user_engagement = {}

# Function to process story interactions
def process_story_interactions(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for story in data.get('story_activities_polls', []) + data.get('story_activities_questions', []) + data.get('story_activities_story_likes', []):
                for interaction in story.get('string_list_data', []):
                    user = interaction.get('value')
                    if user:
                        if user in user_engagement:
                            user_engagement[user] += 1
                        else:
                            user_engagement[user] = 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Process story interactions files
story_interactions_files = [
    'story_interactions/polls.json',
    'story_interactions/questions.json',
    'story_interactions/story_likes.json'
]

for file in story_interactions_files:
    file_path = os.path.join(root_dir, file)
    if os.path.exists(file_path):
        process_story_interactions(file_path)

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, count in user_engagement.items():
            writer.writerow({'User': user, 'Times Engaged': count})
except Exception as e:
    raise IOError(f"Error: Unable to write to the CSV file. {str(e)}")