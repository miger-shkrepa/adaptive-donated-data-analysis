import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root_dir):
    user_engagement = {}
    story_interactions_path = os.path.join(root_dir, "story_interactions")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    if not os.path.exists(story_interactions_path):
        return user_engagement

    for file_name in os.listdir(story_interactions_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(story_interactions_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "story_activities_emoji_quick_reactions" in data:
                        for entry in data["story_activities_emoji_quick_reactions"]:
                            for item in entry["string_list_data"]:
                                user = item["value"]
                                if user in user_engagement:
                                    user_engagement[user] += 1
                                else:
                                    user_engagement[user] = 1
            except json.JSONDecodeError:
                raise ValueError("Error: Failed to decode JSON file.")
            except FileNotFoundError:
                raise FileNotFoundError("Error: The specified JSON file does not exist.")

    return user_engagement

def save_to_csv(user_engagement):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, count in user_engagement.items():
            writer.writerow([user, count])

try:
    user_engagement = get_story_engagement(root_dir)
    save_to_csv(user_engagement)
except Exception as e:
    print(e)