import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Iterate over the story interactions
        story_interactions_dir = os.path.join(root_dir, "story_interactions")
        if os.path.exists(story_interactions_dir):
            for filename in os.listdir(story_interactions_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(story_interactions_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for interaction in data.get("story_activities_polls", []) + data.get("story_activities_questions", []) + data.get("story_activities_quizzes", []) + data.get("story_activities_story_likes", []):
                            title = interaction.get("title")
                            if title:
                                if title not in user_engagement:
                                    user_engagement[title] = 0
                                user_engagement[title] += len(interaction.get("string_list_data", []))

        # Create a CSV file with the user engagement
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["User", "Times Engaged"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, engagement in user_engagement.items():
                writer.writerow({"User": user, "Times Engaged": engagement})

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_user_engagement(root_dir)