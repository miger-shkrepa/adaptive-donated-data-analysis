import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to count story engagements
def count_story_engagements(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    engagement_count = {}

    # Define the paths to the relevant JSON files
    story_likes_path = os.path.join(root_dir, "story_likes.json")
    story_reaction_sticker_reactions_path = os.path.join(root_dir, "story_reaction_sticker_reactions.json")
    polls_path = os.path.join(root_dir, "polls.json")
    questions_path = os.path.join(root_dir, "questions.json")
    quizzes_path = os.path.join(root_dir, "quizzes.json")

    # Helper function to process JSON files
    def process_json_file(file_path):
        if not os.path.exists(file_path):
            return
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data.get("story_activities_story_likes", []):
                for entry in item.get("string_list_data", []):
                    user = entry.get("value")
                    if user:
                        engagement_count[user] = engagement_count.get(user, 0) + 1

    # Process each JSON file
    process_json_file(story_likes_path)
    process_json_file(story_reaction_sticker_reactions_path)
    process_json_file(polls_path)
    process_json_file(questions_path)
    process_json_file(quizzes_path)

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in engagement_count.items():
            writer.writerow({'User': user, 'Times Engaged': count})

# Execute the function
count_story_engagements(root_dir)