import os
import json
import csv

root_dir = "root_dir"

def analyze_story_engagement(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    engagement_count = {}

    # Define the paths to the story interaction files
    story_files = [
        "shopping/story_sticker_interactions/emoji_sliders.json",
        "shopping/story_sticker_interactions/polls.json",
        "shopping/story_sticker_interactions/questions.json",
        "shopping/story_sticker_interactions/quizzes.json",
        "shopping/story_sticker_interactions/story_likes.json"
    ]

    for file_path in story_files:
        full_path = os.path.join(root_dir, file_path)
        if not os.path.exists(full_path):
            continue

        with open(full_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("Error: Invalid JSON format in file {}".format(full_path))

            for activity in data.values():
                for item in activity:
                    user = item.get("title", "Unknown")
                    if user not in engagement_count:
                        engagement_count[user] = 0
                    engagement_count[user] += len(item.get("string_list_data", []))

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, count in engagement_count.items():
            writer.writerow({'User': user, 'Times Engaged': count})

if __name__ == "__main__":
    analyze_story_engagement(root_dir)