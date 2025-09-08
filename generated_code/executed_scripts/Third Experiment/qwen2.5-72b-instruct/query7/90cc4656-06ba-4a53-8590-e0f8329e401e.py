import os
import json
import csv

root_dir = "root_dir"

def process_story_interactions(root):
    user_engagement = {}
    story_likes_path = os.path.join(root, "story_interactions", "story_likes.json")
    countdowns_path = os.path.join(root, "story_interactions", "countdowns.json")

    def parse_story_likes(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                for activity in data.get("story_activities_story_likes", []):
                    for entry in activity.get("string_list_data", []):
                        if "value" in entry:
                            user = entry["value"]
                            user_engagement[user] = user_engagement.get(user, 0) + 1

    def parse_story_countdowns(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                for activity in data.get("story_activities_countdowns", []):
                    for entry in activity.get("string_list_data", []):
                        if "value" in entry:
                            user = entry["value"]
                            user_engagement[user] = user_engagement.get(user, 0) + 1

    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        parse_story_likes(story_likes_path)
        parse_story_countdowns(countdowns_path)

        if not user_engagement:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
        else:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
                for user, count in user_engagement.items():
                    writer.writerow([user, count])

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Call the function with the root directory
process_story_interactions(root_dir)