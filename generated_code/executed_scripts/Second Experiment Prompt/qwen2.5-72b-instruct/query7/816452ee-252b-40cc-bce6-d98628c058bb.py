import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def process_story_interactions(data):
    story_engagements = {}
    for story_type in [
        "story_activities_emoji_quick_reactions",
        "story_activities_questions",
        "story_activities_quizzes",
        "story_activities_polls",
        "story_activities_story_likes",
        "story_activities_reaction_sticker_reactions"
    ]:
        if story_type in data:
            for entry in data[story_type]:
                for item in entry.get("string_list_data", []):
                    username = item.get("value")
                    if username:
                        story_engagements[username] = story_engagements.get(username, 0) + 1
    return story_engagements

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        story_interactions_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
        if not os.path.exists(story_interactions_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
            return

        story_interactions_files = [
            "emoji_story_reactions.json",
            "questions.json",
            "quizzes.json",
            "polls.json",
            "story_likes.json",
            "story_reaction_sticker_reactions.json"
        ]

        story_engagements = {}
        for file_name in story_interactions_files:
            file_path = os.path.join(story_interactions_path, file_name)
            if os.path.exists(file_path):
                data = load_json_file(file_path)
                story_engagements.update(process_story_interactions(data))

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, count in story_engagements.items():
                writer.writerow([user, count])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()