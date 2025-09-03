import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to process the directory and count story engagements
def count_story_engagements(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    story_engagements = {}

    # Define the paths to the relevant JSON files
    story_files = [
        os.path.join(root_dir, "story_interactions", "emoji_sliders.json"),
        os.path.join(root_dir, "story_interactions", "polls.json"),
        os.path.join(root_dir, "story_interactions", "questions.json"),
        os.path.join(root_dir, "story_interactions", "quizzes.json"),
        os.path.join(root_dir, "story_interactions", "story_likes.json")
    ]

    # Process each story interaction file
    for file_path in story_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    for activity in data.values():
                        for item in activity:
                            title = item.get("title", "")
                            if title:
                                if title not in story_engagements:
                                    story_engagements[title] = 0
                                story_engagements[title] += len(item.get("string_list_data", []))
                except json.JSONDecodeError:
                    raise ValueError(f"Error: Invalid JSON format in file {file_path}.")

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, count in story_engagements.items():
            writer.writerow({'User': user, 'Times Engaged': count})

# Execute the function
count_story_engagements(root_dir)